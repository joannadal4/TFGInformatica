import requests

def downloadfile(link: str, file: str):
    response = requests.get("link")
    with open("file", "wb") as file:
        file.write(response.content)
    file.close()
