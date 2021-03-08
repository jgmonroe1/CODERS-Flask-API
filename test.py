import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "tables/nodes")

for row in response.json():
    print(row)
    break