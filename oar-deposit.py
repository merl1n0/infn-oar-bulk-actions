import requests
import yaml
import sys
import urllib.parse
import json
import os
from os.path import exists as file_exists
from dotenv import load_dotenv

# Choose a target host
oar_host = "www.openaccessrepository.it"
cern_host = "sandbox.zenodo.org"
HOST = oar_host

# Choose a token
load_dotenv()  # get environment variables from possible .env file
TOKEN = os.environ.get("OAR_TOKEN", None)

if not TOKEN:
    print("Could not find a valid INVENIORDM_TOKEN env variable or .env config file")
    exit(-1)

params = {'access_token': TOKEN}
headers = {"Content-Type": "application/json"}


# Load metadata from YAML file
if len(sys.argv) < 2:
    print("please provide a file .yaml to read records' metadata")
    exit(-1)
yaml_file = sys.argv[1]

try:
    with open(yaml_file) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        records = yaml.load(file, Loader=yaml.FullLoader)
        yaml_path = os.path.dirname(file.name)

except:
    print("Cannot read ", yaml_file)
    exit(-1)

if len(records) == 0:
    print("no records found")
    exit(-1)
print(f"Found {len(records)} records")


# se non viene passato alcun indice viene caricato il primo record del file .yaml
if len(sys.argv) == 3:
    r = records[int(sys.argv[2])]
else:
    r = records[0]


# Costruiamo il nome del file su OAR in base al titolo ed al path del record

filename = r['title'].replace(' ', '-').lower()
filename += '_' + r['files'][0]['path'].replace('/', '_')
filename = urllib.parse.quote(filename)
# relative paths are built starting from the location of the YAML file
path = yaml_file + r['files'][0]['path']
print(f"\nUploading '{r['title']}' as {filename}")


# Check if file exists
if not file_exists(path):
    print(f"{path} doesn't exists")
    exit(-1)


api = "/api/deposit/depositions"
deposit_url = f'https://{HOST}{api}'

req = requests.post(deposit_url, params=params, json={})
# Headers are not necessary here since "requests" automatically
# adds "Content-Type: application/json", because we're using
# the "json=" keyword argument
# headers=headers,
# headers=headers)


if req.status_code != 201:
    print("Some error occurred")
    print(req.json())
    exit(-1)

deposition_id = req.json()['id']
reserved_doi = req.json()['metadata']['prereserve_doi']['doi']

print(f"Preserved DOI {reserved_doi} for deposition {deposition_id}")

bucket_url = req.json()["links"]["bucket"]


upload_url = f'{bucket_url}/{filename}'
print(f"Upload to '{upload_url}'")


# Let's upload the first file in the files attributes
# The target URL is a combination of the bucket link with the desired filename
# seperated by a slash.
try:
    with open(path, "rb") as fp:
        req = requests.put(
            upload_url,
            data=fp,
            params=params,
        )
except:
    print("Error trying to read the file from ", path)
    exit(-1)

# TODO: controllare se upload termina con successo

# eliminiamo la sezione files dagli attributi
del r['files']

data = {'metadata': r}
print("Metadata: \n", yaml.dump(r))


url = f'{deposit_url}/{deposition_id}'
req = requests.put(url,
                   params=params, data=json.dumps(data),
                   headers=headers)

if req.status_code != 200:
    print("Some error occurred", req.json()['message'], req.json()['errors'])
    exit(-1)


# Per pubblicare il record
#publish_url = f'{deposit_url}/{deposition_id}/actions/publish'
#req = requests.post(publish_url, params=params )
