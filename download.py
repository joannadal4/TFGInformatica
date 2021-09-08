import requests

def download_file(**kwargs):
    """download the required content and save in a file"""
    for file_name, link in kwargs.items():
        response = requests.get(link)
        with open(file_name, "wb") as file:
            file.write(response.content)


if __name__ == "__main__":

    files = {'uniprot.fasta':'https://www.uniprot.org/uniprot/?query=taxonomy:%22Viruses%20[10239]%22%20AND%20reviewed:yes&format=fasta&sort=score',
    'protein-interaction-virus-host.txt':'https://bioinfo.uib.es/~recerca/TFGJoanNadal/protein-interaction-virus-host.txt',
    'protein_host_mapping.txt':'https://bioinfo.uib.es/~recerca/TFGJoanNadal/protein_host_mapping.txt',
    'protein_virus_mapping.txt':'https://bioinfo.uib.es/~recerca/TFGJoanNadal/protein_virus_mapping.txt',
    'final_list.hmms':'https://img.jgi.doe.gov//docs/final_list.hmms'}

    download_file(**files)
