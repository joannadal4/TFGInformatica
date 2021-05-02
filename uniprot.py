import requests
from typing import List
import xml.dom.minidom
from xml.etree import ElementTree

from time import sleep
from db import Session
from models import Function, Protein, R_Protein_Function
from sqlalchemy.sql import exists

import json


def get_go_functions(protein: str) -> List[str]:
    """Given a protein get it GO functions from Uniprot."""
    go_functions = []
    try:
        response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
    except:
        print("Let me sleep for 5 seconds")
        sleep(5)
        print("Was a nice sleep, now let me continue...")
        response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
    # parse xml and return GO
    root = ElementTree.fromstring(response.content)
    session= Session()

    goFunction = root.findall('.//{http://uniprot.org/uniprot}dbReference[@type="GO"]')
    for child in goFunction:
        go_functions.append(child.attrib['id'])
        try:
            resp = requests.get(f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{child.attrib['id']}/complete")
        except:
            print("Let me sleep for 5 seconds")
            sleep(5)
            print("Was a nice sleep, now let me continue...")
            resp = requests.get(f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{child.attrib['id']}/complete")
            continue
        jsonGO = resp.json()
        data_string = json.dumps(jsonGO)
        description= str(json.loads(data_string)["results"][0]["definition"]["text"])
        aspect= str(json.loads(data_string)["results"][0]["aspect"])

        if session.query(exists().where(Function.codeGO == child.attrib['id'])).scalar() == False:
            function = Function(codeGO = child.attrib['id'], description = description, aspect = aspect)
            session.add(function)

        idProtein = session.query(Protein.idProtein).filter(Protein.code == protein)
        idFunction = session.query(Function.idFunction).filter(Function.codeGO == child.attrib['id'])
        if session.query(exists().where(R_Protein_Function.idProtein == idProtein and R_Protein_Function.idFunction == idFunction)).scalar() == False:
            function_protein = R_Protein_Function(idProtein = idProtein, idFunction = idFunction)
            session.add(function_protein)

    session.commit()
    return go_functions





def get_name_specie(protein: str) -> str:
    """Given a protein get it GO functions from Uniprot.    (Important separar get_name i get_code )
    code = ""

1. parse xml to search specie name from xml, if there is parentheses, ignore it
2- Search on http://viruses.string-db.org/download/species.v10.5.txt if specie exists (descarregar)
3- If not exists, then code = null
4- Obtain code of this specie. Regular expression to take the code

    return code"""
