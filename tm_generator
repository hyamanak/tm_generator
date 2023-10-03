import requests, os, csv, re, json, gspread, time, requests
from datetime import datetime, date
from Authenticate import Authenticate
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

script_dicrecotry = os.path.dirname(os.path.abspath(__file__))

class GetFiles():
    ## download jp runsheet
    def __init__(self):
        self.__extension = ".csv"
        self.__date = datetime.today().strftime("%Y-%m-%d")
    
        self.file_name = self.__date + "_jp" + self.__extension
        self.__file_path = os.path.join(script_dicrecotry, self.file_name)
        self.__runsheet_key = '1SU3myyfzFIirzRmR4Vo5uYbSR_vBCAzER0oE0_ENx0o'
        self.__credential = os.path.join(script_dicrecotry, "credential.json")
        self.__runsheet_sheet = 'Documentation'

        self.download_csv_from_jp_runsheet()

    def download_csv_from_jp_runsheet(self):
        gc = gspread.service_account(filename=self.__credential)
        # Open the Japanese RunSheet
        spreadsheet = gc.open_by_key(self.__runsheet_key)
        # Get the first sheet in the spreadsheet
        worksheet = spreadsheet.worksheet(self.__runsheet_sheet)
        # Get all values from the sheet
        data = worksheet.get_all_values()
        ##convert to csv format
        jp_data = '\n'.join([','.join(row) for row in data])
        with open(self.__file_path, 'w+', encoding='utf-8') as jp_file:
            jp_file.write(jp_data)
    
class TmGenerator():
    def __init__(self, runsheet):
        self.date = date.today().strftime('%Y-%m-%d')
        self.tm_name = str(date.today().strftime('%Y-%m-%d')) + '_en_jp'
        self.job_pattern = r"(?<=/job/)(?:[a-zA-Z0-9]+)"
        self.project_pattern = r"(?<=/show/)(?:[a-zA-Z0-9]+)"
        
        self.tmx_directory = "tmx_files"

        self.jp_data = runsheet
        self.job_status = ['DELIVERED', 'COMPLETED']
        self.version = ['Latest', 'PreR']
        self.jp_dict_data = self.csv_to_dict()
        self.project_urls = self.get_project_urls()
        self.project_ids = self.get_project_ids()

        self.job_export_url = 'https://cloud.memsource.com/web/api2/v1/projects/{project_id}/jobs/bilingualFile?format=TMX'
        self.job_url = 'https://cloud.memsource.com/web/api2/v2/projects/{projectUid}/jobs'

        self.token = None
        self.set_token()

        self.tm_id = None

        self.headers = {'Authorization': 'ApiToken ' + self.token,
                        'Content-Type': 'application/json'}

        #self.jp_csv = '0618_jp.csv'
        #self.csv_dict = self.csv_to_dict()
        #self.project_job_ids = self.get_completed_job()

    def set_token(self):
        authenticate = Authenticate()
        self.token = authenticate.token

    def create_new_tm(self):
        create_tm_url = 'https://cloud.memsource.com/web/api2/v1/transMemories'
        data = {"name":self.tm_name,
                "sourceLang":"ja",
                "targetLangs":["en_US"]}

        response = requests.post(create_tm_url, headers=self.headers, json=data)

        if response.status_code == 201:
            self.tm_id = response.json()['id']
            print(f'New TM created with ID: {self.tm_id}')
        else:
            print('Failed to create the new Translation Memory.')
            print(f'Status code: {response.status_code}')
            print(f'Response: {response.text}')

    def export_jobs(self):
        # Import jobs to the Translation Memory
        if not os.path.exists('tmx'):
            os.makedirs('tmx') 
        
        for pid in self.project_ids:
            job_data = self.get_jobs(pid)
            if 'errorCode' in job_data:
                continue

            job_uids = self.get_job_uids(job_data)
            if 'errorCode' in job_uids:
                continue
            for job_uid in job_uids:
                url = self.job_export_url.format(project_id=pid)
                data = json.dumps({
                    "jobs": [{"uid": job_uid}]
                        })
                response = requests.request("POST", url, headers=self.headers, data=data)

                if response.status_code == 200:
                    # Save the TMX file
                    tmx_filename = f'{job_uid}.tmx'
                    directory_path = os.path.join(script_dicrecotry, self.tmx_directory)
                    file_path = os.path.join(directory_path, tmx_filename)
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f'Job with ID {job_uid} (pid {pid}) exported successfully as {tmx_filename}.')
                else:
                    print(f'Failed to export the job with ID {job_uid}.')
                    print(f'Status code: {response.status_code}')
                    print(f'Response: {response.text}')

    def csv_to_dict(self):
            reader = csv.reader(self.jp_data)
            headers = next(reader)  # Read the first line as headers
            return [dict(zip(headers, row)) for row in reader]
            
    def get_project_urls(self):
        #get a list of project URLs that has marked as Done
        added_projects = []
        for item in self.jp_dict_data:
            if item['Ver.'] in ['Latest', 'PreR']:
                phrase_project = item['Phrase project']
                if phrase_project not in added_projects:
                    added_projects.append(phrase_project)
        return added_projects

    def get_id(self, url):
        #get a job id
        pattern = self.project_pattern if '/show/' in url else self.job_pattern if '/job/' in url else None
        match = re.search(pattern, url)
        if match:
            extracted_value = match.group()
            return extracted_value
    
    def get_project_ids(self):
        return [matched_pattern for url in self.project_urls for matched_pattern in re.findall(self.project_pattern, url)]
    
    def get_jobs(self, pid):
        url = self.job_url.format(projectUid=pid)
        param= {"take": 1000}

        response = requests.get(url, headers=self.headers, params=param)
        response_json = response.json()
        return response_json
    
    def get_job_uids(self, job_data):
        #data = json.loads(job_data)
        job_uids = [job["uid"] for job in job_data["content"] if job["status"] in ["DELIVERED", "COMPLETED"]]
        uids = [uid for uid in job_uids]
        return uids
        

runsheet = GetFiles()
file = runsheet.file_name
jp_file = os.path.join(script_dicrecotry, file)

with open(jp_file, 'r', encoding='utf-8') as runsheet:
    tm = TmGenerator(runsheet)
    tm.export_jobs()
    

    ##TODO 2: acess to each project and get job data 
    ##TODO 3: check if job status is 100%
    ##TODO 4: if status is 100% download them as tmx file
    ##TODO 5: make just one tmx 
    ##TODO 6: upload
    
