#!/usr/bin/env python3


import os,sys
import psycopg2
import json

dbc = psycopg2.connect(database='zenodo', user='zenodo', password='zenodo', host = 'localhost', port=5434)
curs=dbc.cursor()

jfn = 'recognizedAuthor.json'

jf = json.load(open(jfn,'r'))


