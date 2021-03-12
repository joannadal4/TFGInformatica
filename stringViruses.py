

def get_proteins_host(protein: str, code: str) -> List[str]:
"""
1- from f"https://www.uniprot.org/uniprot/?query=accession:{protein}&format=xml", parse xml to obtain the name of protein uniprot/entry/name
2- download interactions f"http://viruses.string-db.org/download/protein.links.v10.5/{code}.protein.links.v10.5.txt.gz"
3- unzip the file
4- get interactions from protein calling get_interactions(name_protein:str, file:str) --> List(str)
5- for every interaction requests f"https://string-db.org/api/json/get_string_ids?identifiers={interaction}", is a json
6- Obtain protein host using this json calling get_code_protein_host(json: str)
7- remove(json)
8- proteins_host.append(code_protein_host)
9- remove(file)
"""
return proteins_host



def get_interactions(name_protein: str, file: str) -> List[str]:
"""
1- interactions[]
2- open file and take the code_String_interactions of second column whose code of first column contain the name_protein
3- interactions.append(code_String_interactions)
4- close file
"""
return interactions



def get_code_protein_host(json: str) -> str:
"""
1- code_protein_host
2- open file json
3- obtain taxonName, PreferedName
4- Obtain code protein host with regular expresion using f"https://www.uniprot.org/uniprot/?query=gene:{preferedName} AND organism:{taxonName} AND reviewed:yes&format=fasta
"""
return code_protein_host
