import requests
import json

url = "https://api.example.com/v1/chat/completions"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

with requests.post(url, headers=headers, stream=True) as r:
    for line in r.iter_lines():
        if line:
            obj = json.loads(line.decode("utf-8"))
            print(obj.get("response", ""), end="", flush=True)
