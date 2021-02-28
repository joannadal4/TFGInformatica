import requests


def get_go_functions(protein: str) -> set(str):
    """Given a protein get it GO functions from Uniprot."""
    response = requests.get(f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml")
    # parse xml and return GO
    go_functions = []
    return go_functions
