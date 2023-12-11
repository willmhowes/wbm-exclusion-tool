import os
import requests
import yaml
import json
import pythonwhois
from dotenv import load_dotenv

load_dotenv()

with open("urls.yml", "r") as stream:
    try:
        urls = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

responses = []

for i, earl in enumerate(urls[0:2]):
    if os.path.isfile(f"whoistest/{earl}.json"):
        continue

    print("requesting", earl)
    whois_response = pythonwhois.net.get_root_server(earl)
    print("root server:", whois_response)

    whois_response = pythonwhois.get_whois(earl)
    print("raw:", whois_response)

    # whois_response = requests.get(
    #     whois_request, headers={"Authorization": "Bearer " + os.getenv('API_KEY')}
    # ).json()
    # whois_response["count"] = i + 1

    # responses.append(whois_response)

    # with open(f"whoistest/{earl}.json", "w", encoding="utf-8") as f:
    #     json.dump(whois_response, f, indent=2)
