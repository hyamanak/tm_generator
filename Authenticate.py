import requests, pickle, os
from datetime import datetime, timedelta

##authentication for Phrase to get token

class Authenticate():
    def __init__(self):
        self.token_file = "token.pickle"
        self.token_expiration_time = timedelta(hours=12)

        self.username = None
        self.password = None

        self.token = self.authenticate()

    def set_credential(self):
        self.username = input("Please insert username: ")
        self.password = input("please input password: ")

    def authenticate(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token_file:
                saved_token, expiration_time = pickle.load(token_file)
                if datetime.now() < expiration_time:
                    return saved_token
        
        self.set_credential()

        auth_url = 'https://cloud.memsource.com/web/api2/v1/auth/login'
        auth_data = {
            'userName': self.username,
            'password': self.password
        }

        response = requests.post(auth_url, json=auth_data)

        if response.status_code == 200:
            token = response.json()['token']
            expiration_time = datetime.now() + self.token_expiration_time

            with open(self.token_file, 'wb') as token_file:
                pickle.dump((token, expiration_time), token_file)

            return token

        else:
         raise ValueError("Failed to authenticate")

