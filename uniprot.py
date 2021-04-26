import requests
from typing import List
import xml.dom.minidom
from xml.etree import ElementTree

import psycopg2
from psycopg2 import Error
from psycopg2 import sql

from constant import REGEX_SPECIE


def get_go_functions(protein: str, model: str) -> List[str]:
    """Given a protein get it GO functions from Uniprot."""
    go_functions = []
    response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
    # parse xml and return GO
    root = ElementTree.fromstring(response.content)
    for child in root.iter('*'):
        if 'organism' in child.tag:
            if 'scientific' in child.attrib['type']:
                print(child.attrib['type'])
        if 'dbReference' in child.tag:
            if 'GO' in child.attrib['type']:
                go_functions.append(child.attrib['id'])
    return go_functions

def get_name_specie(protein: str) -> str:
    """Given a protein get it GO functions from Uniprot.    (Important separar get_name i get_code )
    code = ""

1. parse xml to search specie name from xml, if there is parentheses, ignore it
2- Search on http://viruses.string-db.org/download/species.v10.5.txt if specie exists (descarregar)
3- If not exists, then code = null
4- Obtain code of this specie. Regular expression to take the code

    return code"""



"""conn = psycopg2.connect("dbname=%s user=%s  port=%s host=%s password=%s" % (db_name,user, db_port,db_host,password))
cur = conn.cursor()
cur.execute("INSERT INTO MODEL (code, path) VALUES (%s,%s)", (model_name,f"data/models_hmm/{model_name}.hmm"))
conn.commit()
cur.close()
conn.close()"""
