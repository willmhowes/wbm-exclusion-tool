import os
import requests
import yaml
import json

with open("urls.yml", "r") as stream:
    try:
        urls = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

responses = []

for earl in urls:
    if os.path.isfile(f"iacdx/{earl}.json"):
        continue

    ia_request = f"https://web.archive.org/cdx/search/cdx?url={earl}&fl=timestamp&output=json&limit=1"

    print("requesting", earl)

    ia_response = requests.get(ia_request).json()

    responses.append(ia_response)

    with open(f"iacdx/{earl}.json", "w", encoding="utf-8") as f:
        json.dump(ia_response, f, indent=2)
