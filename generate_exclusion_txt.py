import yaml
import json
import datetime
from csv import DictReader

with open("urls.yml", "r") as stream:
    try:
        urls = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open("domainsanddates.csv", "r") as f:
    dict_reader = DictReader(f)
    creation_dates = {entry["domain"]: entry["date"] for entry in list(dict_reader)}

final_data = []

for i, earl in enumerate(urls):
    with open(f"whois/{earl}.json", "r", encoding="utf-8") as f:
        whois_response = json.load(f)
        with open(f"iacdx/{earl}.json", "r", encoding="utf-8") as f:
            ia_response = json.load(f)

            if len(ia_response) > 0:
                ia_earliest_date = ia_response[1][0]
                ia_earliest_date = (
                    ia_earliest_date[0:4]
                    + "-"
                    + ia_earliest_date[4:6]
                    + "-"
                    + ia_earliest_date[6:8]
                )
                ia_earliest_date = datetime.date.fromisoformat(ia_earliest_date)

            # strip time information from whois datetime
            whois_creation_date = whois_response["domain"]["created_date"]
            whois_creation_date = datetime.datetime.fromisoformat(whois_creation_date)
            whois_creation_date = datetime.date.fromisoformat(
                whois_creation_date.date().isoformat()
            )

            # insert provided ownership if available
            if creation_dates[earl] != "N/A":
                ownership_date = datetime.date.fromisoformat(creation_dates[earl])
                creation_is_earlier = ownership_date < ia_earliest_date
                whois_used = False
            else:
                creation_is_earlier = whois_creation_date < ia_earliest_date
                whois_used = True

            # convert dates to useful strings
            whois_creation_date = whois_creation_date.isoformat()
            ia_earliest_date = ia_earliest_date.isoformat()

            final_data.append(
                (
                    i,
                    earl,
                    ia_earliest_date,
                    whois_creation_date,
                    creation_is_earlier,
                    whois_used,
                )
            )


with open(f"exclusion.txt", "w", encoding="utf-8") as f:
    f.write("# Ownership date is after earliest WBM date\n")
    f.write("\n")
    for obj in final_data:
        num, url, ia, who, creation_is_earlier, whois_used = obj
        if not creation_is_earlier and not whois_used:
            f.write(url + "\n")
            f.write("marc@diginov.fr\n")
            f.write(creation_dates[url] + "\n")
            f.write(
                "Per Present Website Owner, Marc DE ZORDO, marc@diginov.fr, Provided pdf of invoice demonstrating domain ownership, "
                + f"excludefor:{datetime.date.fromisoformat(creation_dates[url]).strftime('%Y%m%d')}-future\n"
            )
            f.write("Generated ID: \n\n")

    # Per Present Website Owner, <FULL NAME IF PROVIDED>, <EMAIL ADDRESS>, <HOW REQUESTER SATISFIED VERIFICATION>, excludefor:YYYYMMDD-YYYYMMDD

    f.write("\n")

    f.write("# No ownership proven")
    f.write("\n")
    for obj in final_data:
        num, url, ia, who, creation_is_earlier, whois_used = obj
        if whois_used:
            f.write("- " + url + "\n")
            f.write(
                "   - Start of Ownership                     : "
                + creation_dates[url]
                + "\n"
            )
            f.write("   - Earliest date found in Wayback Machine : " + ia + "\n")
            f.write("   - Creation date according to WHOIS lookup: " + who + "\n")
