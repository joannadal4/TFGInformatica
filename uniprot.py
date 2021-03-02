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
    print(protein)
    for child in root.iter('*'):
        if 'dbReference' in child.tag:
            if 'GO' in child.attrib['type']:
                go_functions.append(child.attrib['id'])
    return go_functions
