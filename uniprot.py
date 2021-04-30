import requests
from typing import List
import xml.dom.minidom
from xml.etree import ElementTree

import json


def get_go_functions(protein: str) -> List[str]:
    """Given a protein get it GO functions from Uniprot."""
    go_functions = []
    response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
    # parse xml and return GO
    root = ElementTree.fromstring(response.content)

    goFunction = root.findall('.//{http://uniprot.org/uniprot}dbReference[@type="GO"]')
    for child in goFunction:
        go_functions.append(child.attrib['id'])
        resp = requests.get(f"https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{child.attrib['id']}/complete")
        jsonGO = resp.json()
        data_string = json.dumps(jsonGO)
        description= str(json.loads(data_string)["results"][0]["definition"]["text"])
        aspect= str(json.loads(data_string)["results"][0]["annotationGuidelines"]["aspect"])

        print(aspect)

    return go_functions





def get_name_specie(protein: str) -> str:
    """Given a protein get it GO functions from Uniprot.    (Important separar get_name i get_code )
    code = ""

1. parse xml to search specie name from xml, if there is parentheses, ignore it
2- Search on http://viruses.string-db.org/download/species.v10.5.txt if specie exists (descarregar)
3- If not exists, then code = null
4- Obtain code of this specie. Regular expression to take the code

    return code"""
