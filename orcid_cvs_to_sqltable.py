#!/usr/bin/env python3

import os,sys
import csv
import psycopg2

csvfile = 'names_orcid_infn.csv'
"""
zenodo=# create table orcid (id bigserial not null primary key, orcid varchar(19) unique not null, email varchar, givenname varchar, familyname varchar,fullname varchar, sede text,pastsede text,credit varchar,othernames varchar);
CREATE TABLE
"""
H='orcid,email,given-names,family-name,given-and-family-names,current-institution-affiliation-name,past-institution-affiliation-name,credit-name,other-names'


dbc = psycopg2.connect(database='zenodo', user='zenodo', password='zenodo', host = 'localhost', port=5434)
curs=dbc.cursor()

sq = """INSERT INTO orcid 
(orcid,email,givenname,familyname,fullname,sede,pastsede,credit,othernames) VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

f = open(csvfile,'r')
csvline  = csv.reader(f)
H = csvline.__next__()
for n,tup in enumerate(csvline):
   #print(curs.mogrify(sq,tuple([x or None for x in tup])))
   L = tuple([x or None for x in tup])
   curs.execute(sq,tuple(L))

dbc.commit()
