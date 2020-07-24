#!/usr/bin/env python3

import sqlite3 # pour PostgreSQL : psycopg2
 # pour MySQL/MariaDB : MysqlDB ou pymysql


from string import ascii_letters, digits
from itertools import chain
from random import choice
import os

def create_uid(n=9):
   '''Génère une chaîne de caractères alétoires de longueur n
   en évitant 0, O, I, l pour être sympa.'''
   chrs = [ c for c in chain(ascii_letters,digits)
                        if c not in '0OIl'  ]
   return ''.join( ( choice(chrs) for i in range(n) ) ) 

def Insert_into_db(uid=None,code=None,language=None):
    '''Crée/Enregistre le document dans le db. Return the file name.
    '''
    if uid is None:
        uid = create_uid()
        code = '# Write your code here...'

    with sqlite3.connect('script.sqlite3') as conn:
        curs = conn.cursor()
        curs.execute('INSERT INTO script VALUES (?,?,?)',(uid,code,language))
        conn.commit()
        
    return uid

def SELECT_form_db(uid):
    '''Lit le document data/uid'''
    try:
        with sqlite3.connect('script.sqlite3') as conn:
            curs = conn.cursor()
            curs.execute('SELECT * FROM script WHERE uid = ?',(uid))
    except FileNotFoundError:
        return None

def get_last_entries_from_files(n=10,nlines=10):
    entries = os.scandir('data')
    d = []
    entries = sorted(list(entries),
                     key=(lambda e: e.stat().st_mtime),
                     reverse=True) 
    for i,e in enumerate(entries):
        if i >= n:
            break
        if e.name.startswith('.'):
            continue
        with open('data/{}'.format(e.name)) as fd:
            code = ''.join(( fd.readline() for i in range(nlines) ))
            if fd.readline():
                code += '\n...'
        d.append({ 'uid':e.name, 'code':code })
    return d

