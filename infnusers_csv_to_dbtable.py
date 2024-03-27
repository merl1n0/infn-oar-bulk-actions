#!/usr/bin/env python3

"""feed infnusers.csv in a service table in the zenodo DB"""

import psycopg2
import os,sys

dbc = psycopg2.connect(database='zenodo', user='zenodo', password='zenodo', host = 'localhost', port=5434)
curs=dbc.cursor()

# CREATE TABLE infnusers (id serial not null primary key, nome varchar, email varchar, sede varchar);
sq = """INSERT INTO infnusers (nome, email, sede) VALUES (%s,%s,%s)"""
f = open('users-1.csv','r')
for l in f:
    tup = l.strip().split(',')
    sede = tup.pop()
    email = tup.pop()
    nome = ' '.join(tup)
    curs.execute(sq,(nome, email, sede))

f.close()
dbc.commit()
dbc.close()
