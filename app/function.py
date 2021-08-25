import requests
from typing import List
import xml.dom.minidom
from xml.etree import ElementTree

from time import sleep
from db import Session
from models import Function, Protein, R_Protein_Function
from sqlalchemy.sql import exists, and_

import json


def get_go_functions(protein: str):
    """Given a protein get it GO functions from Uniprot."""
    go_functions = []
    session= Session()

    idProtein = session.query(Protein.idProtein).filter(Protein.codeUniprot == protein).scalar()
    if idProtein is not None:
        if session.query(exists().where(R_Protein_Function.c.idProtein == idProtein)).scalar() == False:
            try:
                response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
            except:
                sleep(5)
                response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")

            try:
                root = ElementTree.fromstring(response.content)

                go_function = root.findall('.//{http://uniprot.org/uniprot}dbReference[@type="GO"]')
                for child in go_function:
                    go_functions.append(child.attrib['id'])
                    try:
                        resp = requests.get(f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{child.attrib['id']}/complete")
                    except:
                        sleep(5)
                        resp = requests.get(f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{child.attrib['id']}/complete")
                        continue

                    json_GO = resp.json()
                    json_GO_format = json.loads(json.dumps(json_GO))

                    description= str(json_GO_format["results"][0]["definition"]["text"])
                    aspect= str(json_GO_format["results"][0]["aspect"])

                    if session.query(exists().where(Function.codeGO == child.attrib['id'])).scalar() == False:
                        function = Function(codeGO = child.attrib['id'], description = description, aspect = aspect)
                        session.add(function)
                        session.commit()

                    idFunction = session.query(Function.idFunction).filter(Function.codeGO == child.attrib['id']).scalar()
                    if session.query(exists().where(and_(R_Protein_Function.c.idProtein == idProtein, R_Protein_Function.c.idFunction == idFunction))).scalar() == False:
                        function_protein = R_Protein_Function.insert().values(idProtein = idProtein, idFunction = idFunction)
                        session.execute(function_protein)
                        session.commit()

            except:
                print(f"The protein {protein} is unaccessible")

    session.close()
