from pprint import pprint
import csv, json
import psycopg2

fn = 'v1.41-2024-02-13-ror-data.csv'
f=open(fn,'r')

csvr = csv.reader(f)
H = next(csvr)
R=[]
for r in csvr:
   R.append(r)

K0 = ['id','name','acronyms','country.country_code']
K1 = ['id','name','acronym']

dbc = psycopg2.connect(host='localhost', database='oarfull', user='oarfull', password='oarfull', port=5434)
curs=dbc.cursor()

sq = """INSERT INTO affiliation_metadata VALUES (now(),now(),gen_random_uuid(),%s,2)"""

for n,r in enumerate(R,1):
    d = dict(zip(H,r))
    dtemp = {"id": d['id'].split('/')[-1],
        "pid": {"pk": n, "status": "R", "obj_type": "rec", "pid_type": "aff"},
        "name": d['name'],
        "title": {d['country.country_code']: d['name']},
        "$schema": "local://affiliations/affiliation-v1.0.0.json",
        "acronym": d['acronyms'],
        "identifiers": [{"scheme": "ror",
        "identifier": d['id'].split('/')[-1]}]}
    #print(curs.mogrify(sq,(json.dumps(dtemp),)))
    curs.execute(sq,(json.dumps(dtemp),))