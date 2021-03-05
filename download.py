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

if __name__ == "__main__":
    #downloadUniprot()
    downloadModels()
