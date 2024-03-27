#!/usr/bin/env python3

import os,sys
import csv
import psycopg2

csvfile = 'v1.41-2024-02-13-ror-data.csv'
"""
zenodo=# create table ror (id bigserial not null primary key, ror varchar(10) unique not null, 
 name varchar, givenname varchar, familyname varchar,fullname varchar, sede text,pastsede text,credit varchar,othernames varchar);
CREATE TABLE
"""

f = open(csvfile,'r')
csvf = csv.reader()
H = next(csvf)

dbc = psycopg2.connect(database='zenodo', user='zenodo', password='zenodo', host = 'localhost', port=5434)
curs=dbc.cursor()



sq = """INSERT INTO orcid 
(orcid,email,givenname,familyname,fullname,sede,pastsede,credit,othernames) VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

for n,tup in enumerate(csvf):
   d = dict(zip(H,r))
   ror = d['id'].split('/')[-1]
   
   curs.execute(sq,tuple(L))

dbc.commit()
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