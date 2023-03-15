import requests

resp = requests.post("http://0.0.0.0:8080",
                     files=dict(file=open("/home/fulvio/loko/data/targa-auto-italiana-1-780x405.jpg", "rb"), args="{}"))

print(resp.json())
