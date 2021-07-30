import requests

def downloadfile(link: str, file: str):
    response = requests.get("link")
    with open("file", "wb") as file:
        file.write(response.content)
    file.close()



"""
uniprot.fasta  = https://www.uniprot.org/uniprot/?query=taxonomy:%22Viruses%20[10239]%22%20AND%20reviewed:yes&format=fasta&sort=score
final_list.hmms = https://img.jgi.doe.gov//docs/final_list.hmms
interactions.txt = servidor uib
protein_aliases_virus.txt = servidor uib
protein_aliases_host.tsv = servidor uib
"""
