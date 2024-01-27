import json
import os
import hashlib
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Path to your JSON file
json_file_path = 'info.json'

# Function to load JSON data from a file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load and parse the JSON data

# Load JSON data from file
data = load_json_data(json_file_path)

# Function to calculate MD5
def calculate_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to download a file
def download_file(file_info):
    file_id = str(data['dataFile']['id'])
    md5_checksum = file_info['md5']
    url = f"https://dataverse.harvard.edu/api/access/datafile/{file_id}"

    if os.path.isfile(file_id):
        local_md5_checksum = calculate_md5(file_id)
        if local_md5_checksum == md5_checksum:
            print(f"File {file_id} already exists and MD5 checksum matches.")
            return
        else:
            print(f"File {file_id} exists but MD5 checksum does not match. Downloading...")

    print(f"Downloading {file_id}...")
    #subprocess.run(['wget', url, '-O', file_id])

# Using ThreadPoolExecutor to download files in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(download_file, data)
