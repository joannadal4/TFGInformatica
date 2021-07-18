import requests

def downloadUniprot():
    response = requests.get("https://www.uniprot.org/uniprot/?query=taxonomy:%22Viruses%20[10239]%22%20AND%20reviewed:yes&format=fasta&sort=score")
    with open("uniprot.fasta", "wb") as file:
        file.write(response.content)
    file.close()

def downloadModels():
    response = requests.get("https://img.jgi.doe.gov//docs/final_list.hmms")
    with open("final_list.hmms", "wb") as file:
        file.write(response.content)
    file.close()


def downloadInteractions():
    response = requests.get("")
    with open("interactions.txt", "wb") as file:
        file.write(response.content)
    file.close()

def downloadStringProteinVirus():
    response = requests.get("")
    with open("protein_aliases_virus.txt", "wb") as file:
        file.write(response.content)
    file.close()

def downloadStringProteinHost():
    response = requests.get("")
    with open("protein_aliases_host.tsv", "wb") as file:
        file.write(response.content)
    file.close()
