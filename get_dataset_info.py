import requests
import json
# Replace this with the actual base URL of the Dataverse repository
base_url = "https://dataverse.harvard.edu"

# Dataset persistent ID
dataset_persistent_id = "doi:10.7910/DVN/N4VLQL"

# Construct the API request URL for dataset information
api_url = f"{base_url}/api/datasets/:persistentId/?persistentId={dataset_persistent_id}"

# Make the request for dataset information
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    files_info = data['data']['latestVersion']['files']
    with open("info.json", 'w') as file:
        json.dump(files_info, file, indent=4)

    # Loop through each file and download it
    for file_info in files_info:
        file_id = file_info['dataFile']['id']
        download_url = f"{base_url}/api/access/datafile/{file_id}"
        print(download_url)
else:
    print("Failed to retrieve dataset information")

