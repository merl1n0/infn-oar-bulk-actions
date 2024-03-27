
# Importo i moduli necessari
import csv
import yaml

csvfile = 'names_orcid_infn.csv'
yamlfile = 'names_orcid_infn.yaml'

H='orcid,email,given-names,family-name,given-and-family-names,current-institution-affiliation-name,past-institution-affiliation-name,credit-name,other-names'



# Open the CSV file
with open(csvfile,'r') as csvf, open(yamlfile,'w') as yamlf:
    # Read the CSV data
    csv_rows = csv.DictReader(csvf)
    # Convert the CSV data to a list of dictionaries
    #d = {'affiliations' : }
    for d in csv_rows:
        d0 = {''}
    data_list = [row for row in csv_rows]
    s = yaml.dump(data_list)
    yamlf.write(s)
