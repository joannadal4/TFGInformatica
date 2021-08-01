import requests

def downloadfile(link: str, file: str):
    """download the required content and save in a file"""
    response = requests.get("link")
    with open("file", "wb") as file:
        file.write(response.content)
    file.close()
