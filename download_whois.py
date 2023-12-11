import os
import requests
import yaml
import json
from dotenv import load_dotenv

load_dotenv()

# def download_whois():


with open("urls.yml", "r") as stream:
    try:
        urls = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

responses = []

for i, earl in enumerate(urls):
    if os.path.isfile(f"whois/{earl}.json"):
        continue

    whois_request = f"https://whoisjsonapi.com/v1/{earl}"

    print("requesting", earl)

    whois_response = requests.get(
        whois_request, headers={"Authorization": "Bearer " + os.getenv("API_KEY")}
    ).json()
    whois_response["count"] = i + 1

    responses.append(whois_response)

    with open(f"whois/{earl}.json", "w", encoding="utf-8") as f:
        json.dump(whois_response, f, indent=2)
