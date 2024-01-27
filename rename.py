import json
import os
import hashlib

# Function to calculate MD5
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to process each JSON entry
def process_file(data):
    #try:
    file_id = str(data['dataFile']['id'])
    filename = data['dataFile']['filename']
    print(f"{file_id}, {filename}")
    directory_label = ""
    if data.get('directoryLabel'):
        directory_label = data['directoryLabel']
    md5_checksum = data['dataFile']['checksum']['value']

    src = file_id  # Adjust this if your file names are different
    dst = os.path.join(directory_label, filename)

    if os.path.isfile(src):
        # Check MD5
        if md5(src) != md5_checksum:
            print(f"MD5 mismatch for file {filename}, {file_id}")
        #else:
            #print(f"File {filename} processed successfully")
            # Rename and move file
        os.makedirs(directory_label, exist_ok=True)
        os.rename(src, dst)

    #except Exception as e:
        #print(f"Error processing file: {e}, {str(data['dataFile']['id'])}")

# Load JSON data from a file
with open('../info.json', 'r') as file:
    json_data = json.load(file)

for entry in json_data:
    process_file(entry)
