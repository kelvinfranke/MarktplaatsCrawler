import requests

url = "https://api.marktplaats.nl/v1/categories/"
headers = {"Host": "api.marktplaats.nl"}

response = requests.get(url, headers=headers)
print(response)
