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
SESSION = os.environ.get("OAR_SESSION", None)

if not SESSION:
    print("Could not find a valid OAR_SESSION env variable or .env config file")
    exit(-1)

params = {'access_token': TOKEN}
headers = {"Content-Type": "application/json"}


# Load metadata from YAML file
if len(sys.argv) < 4:
    print("\nPlease provide at least a .yml file to read records'metadata from, a <community> identifier and <action> (accept | reject) to issue\n")
    print(
        f"Syntax: python {sys.argv[0]} <path_of_the_yml_file> <community> <action> [record_start_index] [record_end_index]\n")
    exit(-1)
yaml_file = sys.argv[1]
COMMUNITY = sys.argv[2]
ACTION = sys.argv[3]

try:
    with open(yaml_file) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        records = yaml.load(file, Loader=yaml.FullLoader)
        yaml_path = os.path.dirname(file.name)
        # print("yaml_path", yaml_path)

except:
    print("Cannot read ", yaml_file)
    exit(-1)

record_count = len(records)

if record_count == 0:
    print("no records found")
    exit(-1)
print(f"Found {record_count} records in {yaml_file}\n")


# se non viene passato alcun indice viene caricato il primo record del file .yaml
# if len(sys.argv) == 3:
#    r = records[int(sys.argv[2])]
# else:
#    r = records[0]


# per caricare un singolo record usare due volte lo stesso indice

# sys.argv[4]  [record_start_index]
# sys.argv[5]  [record_end_index]

# se non viene passato alcun indice vengono caricati tutti i record
start_index = 0
end_index = record_count - 1
# se viene passato solo indice iniziale (un solo indice) viene caricato dall'i-esimo record alla fine
if len(sys.argv) == 5:
    start_index = int(sys.argv[4])
    if start_index >= record_count:
        print("<record_start_index> greater than available number of records\n")
        exit(-1)
elif len(sys.argv) == 6:
    start_index = int(sys.argv[4])
    end_index = int(sys.argv[5])
    if start_index >= record_count or end_index >= record_count:
        print("<record_start_index> or <record_end_index> greater than available number of records\n")
        exit(-1)


for i in range(start_index, end_index + 1):

    r = records[i]
    print(f"Parsing Record # [{i}] id # {r['id']}")
    if 'title' in r:
        print(f"Title: {r['title']}")

    # req = requests.post(deposit_url, params=params, json={})
    # Headers are not necessary here since "requests" automatically
    # adds "Content-Type: application/json", because we're using
    # the "json=" keyword argument
    # headers=headers,
    # headers=headers)

    # if req.status_code != 201:
    #     print("Some error occurred")
    #     print(req.json())
    #     exit(-1)

    # reserved_doi = req.json()['metadata']['prereserve_doi']['doi']

    # print(f"Preserved DOI {reserved_doi} for deposition {deposition_id}")

    # bucket_url = req.json()["links"]["bucket"]

    # upload_url = f'{bucket_url}/{filename}'
    # print(f"Upload to '{upload_url}'")

    # Let's upload the first file in the files attributes
    # The target URL is a combination of the bucket link with the desired filename
    # seperated by a slash.
    # try:
    #     with open(path, "rb") as fp:
    #         req = requests.put(
    #             upload_url,
    #             data=fp,
    #             params=params,
    #         )
    # except:
    #     print("Error trying to read the file from ", path)
    #     exit(-1)

    # # TODO: controllare se upload termina con successo

    # # eliminiamo la sezione files dagli attributi
    # del r['files']

    # data = {'metadata': r}
    # # print("\nMetadata:\n\n", yaml.dump(r))

    # url = f'{deposit_url}/{deposition_id}'
    # req = requests.delete(url, params=params, headers=headers)

    # Per pubblicare il record
    #publish_url = f'{deposit_url}/{deposition_id}/actions/publish'
    curate_id = r['id']
    data = {'recid': curate_id, 'action': ACTION}
    api = f"/communities/{COMMUNITY}/curaterecord/"
    curate_url = f'https://{HOST}{api}'

    session = requests.session()
    rest_options = {'HttpOnly': True}
    session.cookies.set("session", SESSION,
                        domain="www.openaccessrepository.it", path="/", secure=True, rest=rest_options)
    req = session.post(curate_url, params=params,
                       headers=headers, data=json.dumps(data))

    # print(yaml.dump(req.json()))

    if req.status_code != 200:
        print("status code: ", req.status_code)
        print("Some error occurred:", req.json()
              ['message'])
        if "errors" in req.json():
            print("Errors: ", req.json()['errors'])
        exit(-1)
    else:
        print(
            f"Record # [{i}] id {curate_id} successfully {ACTION}ed into {COMMUNITY}! \n")
