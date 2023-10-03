import glob, os
import xml.etree.ElementTree as ET


script_dicrecotry = os.path.dirname(os.path.abspath(__file__))

# Set the file pattern for TMX files in your directory
file_pattern = '*.tmx'

# Set the output file path for the merged TMX file
output_file_path = os.path.join(script_dicrecotry, 'merged.tmx')

# Create a new root element for the merged TMX file
root = ET.Element('tmx')

# Iterate over each TMX file
for file_path in glob.glob(os.path.join(script_dicrecotry, file_pattern)):
    tree = ET.parse(file_path)
    tmx_root = tree.getroot()

    # Merge the contents of the TMX file into the merged TMX root
    root.extend(tmx_root)

# Create a new tree with the merged root
merged_tree = ET.ElementTree(root)

# Write the merged TMX tree to the output file
merged_tree.write(output_file_path, encoding='utf-8', xml_declaration=True)


print('Merging complete. Merged TMX file saved as:', output_file_path)
