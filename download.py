import requests

def downloadfile(**kwargs):
    """download the required content and save in a file"""
    for file, link in kwargs.items():
        response = requests.get("link")
        with open("file", "wb") as file:
            file.write(response.content)

if __name__ == "__main__":
    downloadfile("uniprot.fasta"="https://www.uniprot.org/uniprot/?query=taxonomy:%22Viruses%20[10239]%22%20AND%20reviewed:yes&format=fasta&sort=score",
    "final_list.hmms"="https://img.jgi.doe.gov//docs/final_list.hmms", "protein-interaction-virus-host.txt"="servidor uib 1",
    "protein_host_mapping.txt"="servidor uib 2", "protein_virus_mapping.txt"="servidor uib 3")
