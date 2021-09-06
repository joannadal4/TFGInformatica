import requests
import io
from googleapiclient.http import MadiaIoBaseDownload

def download_file(**kwargs):
    """download the required content and save in a file"""
    for file, link in kwargs.items():
        response = requests.get(link)
        with open(file, "wb") as file:
            file.write(response.content)

def download_file_from_Drive(*args):
    """download the required content and save in a file"""
    for fileId in args.items():

        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

if __name__ == "__main__":
    #download_file("uniprot.fasta"="https://www.uniprot.org/uniprot/?query=taxonomy:%22Viruses%20[10239]%22%20AND%20reviewed:yes&format=fasta&sort=score",
    #"final_list.hmms"="https://img.jgi.doe.gov//docs/final_list.hmms")

    download_file_from_Drive("1nqjOqY37YV9-dDsYG3vUgacWnBwULiDM", "1drIkUpjAmKoPCAKkZ6RRS18-jhLMZNJN", "1xvz78-7r2SPVWX2Vd8cWNkICxuBPA5dg")
