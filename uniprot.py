import requests
from typing import List
import xml.dom.minidom
from xml.etree import ElementTree


def get_go_functions(protein: str) -> List[str]:
    """Given a protein get it GO functions from Uniprot."""
    go_functions = []
    response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
    # parse xml and return GO
    root = ElementTree.fromstring(response.content)
    for child in root.iter('*'):
        if 'dbReference' in child.tag:
            if 'GO' in child.attrib['type']:
                go_functions.append(child.attrib['id'])
    return go_functions

def get_name_specie(protein: str) -> str:
    """Given a protein get it GO functions from Uniprot."""
    codes = ""
"""
1. parse xml to search specie name from xml, if there is parentheses, ignore it
2- Search on http://viruses.string-db.org/download/species.v10.5.txt if specie exists
3- If not exists, then code = null
4- Obtain code of this specie. Regular expression to take the code
"""
    return code
