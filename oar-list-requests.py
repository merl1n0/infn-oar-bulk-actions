from telnetlib import STATUS
from unittest import result
import requests
import yaml
import sys
import urllib.parse
import json
import os
from os.path import exists as file_exists
from dotenv import load_dotenv
import argparse

# Choose a target host
oar_host = "www.openaccessrepository.it"
cern_host = "sandbox.zenodo.org"
HOST = oar_host

# Choose a token
load_dotenv()  # get environment variables from possible .env file
TOKEN = os.environ.get("OAR_TOKEN", None)

if not TOKEN:
    print("Could not find a valid OAR_TOKEN env variable or .env config file")
    exit(-1)

params = {'access_token': TOKEN}
headers = {"Content-Type": "application/json"}


# Load metadata from YAML file
# if len(sys.argv) < 2:
#     print("\nPlease provide at least a .yml file to read records'metadata from\n")
#     print(
#         f"Syntax: python {sys.argv[0]} [status] [path_of_the_criteria_yml_file] \n")
#     exit(-1)

parser = argparse.ArgumentParser()
parser.add_argument("community", help="identifier of the community")
parser.add_argument(
    "--criteria", help=".yml file that contains filter criteria")
parser.add_argument("--size", type=int,
                    help="number of records to return", default=100)
parser.add_argument("--page", type=int,
                    help="page number", default=1)

args = parser.parse_args()


if args.criteria:
    yaml_file = args.criteria
    try:
        with open(yaml_file) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            criteria = yaml.load(file, Loader=yaml.FullLoader)
            yaml_path = os.path.dirname(file.name)
    except:
        print("Cannot read ", yaml_file)
        exit(-1)


api = "/api/records"
search_url = f'https://{HOST}{api}'

# params['q'] = f"{criteria[0]}"

params['provisional_communities'] = args.community
params['size'] = args.size
params['page'] = args.page
req = requests.get(search_url, params=params)
# Headers are not necessary here since "requests" automatically
# adds "Content-Type: application/json", because we're using
# the "json=" keyword argument
# headers=headers,
# headers=headers)
print(req.request.url)
results = req.json()['hits']['hits']
# print(results)
depositions = []

for r in results:
    record = {
        'id': r['id'],
        'title': r['metadata']['title'],
        'url': r['links']['html'],
        'created': r['created'],
        'doi': r['doi']
    }

    depositions.append(record)
    #record['files'][0]['url'] = r['files'][0]['links']['download']
    print(yaml.dump(record))

# print(yaml.dump(results))
print(f"\nFound {len(results)} records")

if len(results) > 0:
    fname = f"pending-requests-{args.community}.yaml"

    try:
        with open(fname, "w") as out_file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format

            out_file.write(yaml.dump(depositions))

            # yaml_path = os.path.dirname(file.name)
            # print("yaml_path", yaml_path)

    except:
        print("Cannot write output yaml file")
        exit(-1)

"""  if req.status_code != 201:
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
# print("\nMetadata:\n\n", yaml.dump(r))

url = f'{deposit_url}/{deposition_id}'
req = requests.put(url,
                    params=params, data=json.dumps(data),
                    headers=headers)

# print(yaml.dump(req.json()))

if req.status_code != 200:
    print("Some error occurred", req.json()
            ['message'])
    print(req.json()['errors'])
    exit(-1)
else:
    try:
        with open(yaml_file.replace(".yml", "_out.yml"), "a") as out_file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            resp = req.json()
            deposit = {'id': resp['id'], 'title': resp['metadata']
                        ['title'], 'url': resp['links']['html'], 'reserved_doi': reserved_doi}

            out_file.write(yaml.dump([deposit]))

            # yaml_path = os.path.dirname(file.name)
            # print("yaml_path", yaml_path)

    except:
        print("Cannot write ", yaml_file)
        exit(-1)
    print(
        f"Record # [{i}] deposit complete! Edit at: {req.json()['links']['html']}\n")

# Per pubblicare il record
# publish_url = f'{deposit_url}/{deposition_id}/actions/publish'
#req = requests.post(publish_url, params=params ) """
