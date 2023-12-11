import os
import re
import yaml
import datetime
from copy import deepcopy

with open("urls.yml", "r") as stream:
    try:
        urls = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

regx = r"(?:https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?([a-zA-Z0-9\-]{2,}(?:\.[a-zA-Z0-9\-]{2,})*(?:\.[a-zA-Z\-]{2,}))"
prog = re.compile(regx)

filedates = []

filenames = os.listdir("invoices")
for filename in filenames:
    with open(f"invoices/{filename}", "r") as f:
        text_to_scan = f.read()
        # print(text_to_scan)
        domains = re.findall(prog, text_to_scan)

        for candidate_domain in domains:
            candidate_date = filename[:-4]
            candidate_date = datetime.date.fromisoformat(candidate_date)
            found = False
            for i, entry in enumerate(filedates):
                domain, date = entry
                if candidate_domain == domain:
                    found = True
                    date = datetime.date.fromisoformat(date)
                    if candidate_date < date:
                        candidate_date = candidate_date.isoformat()
                        filedates[i] = (candidate_domain, candidate_date)
                        break
            if not found:
                candidate_date = candidate_date.isoformat()
                filedates.append((candidate_domain, candidate_date))

remaining_urls = set(deepcopy(urls))

with open("domainsanddates.csv", "w") as f:
    f.write("domain,date\n")
    for entry in filedates:
        candidate_domain, candidate_date = entry
        if candidate_domain in urls:
            remaining_urls.remove(candidate_domain)
            f.write(candidate_domain)
            f.write("," + candidate_date)
            f.write("\n")
    remaining_urls = list(remaining_urls)
    for remaining_url in remaining_urls:
        f.write(remaining_url)
        f.write(",N/A")
        f.write("\n")
