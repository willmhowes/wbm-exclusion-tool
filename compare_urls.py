import yaml
import json
import datetime
from datetime import date


def was_created_before_earliest_archive(creation_date: date, archive_date: date):
    return creation_date < archive_date


with open("urls.yml", "r") as stream:
    try:
        urls = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

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

            creation_is_earlier = whois_creation_date < ia_earliest_date

            # convert dates to useful strings
            whois_creation_date = whois_creation_date.isoformat()
            ia_earliest_date = ia_earliest_date.isoformat()

            final_data.append(
                (i, earl, ia_earliest_date, whois_creation_date, creation_is_earlier)
            )


with open(f"output.md", "w", encoding="utf-8") as f:
    f.write("# Creation date is before earliest WBM date\n")
    for obj in final_data:
        num, url, ia, who, boolean = obj
        if boolean:
            f.write(url + "\n")
    f.write("\n")
    for obj in final_data:
        num, url, ia, who, boolean = obj
        if boolean:
            f.write("- " + url + "\n")
            f.write("   - Earliest date found in Wayback Machine: " + ia + "\n")
            f.write("   - Creation date according to WHOIS lookup: " + who + "\n")

    f.write("\n")

    f.write("# Creation date is after earliest WBM date\n")
    for obj in final_data:
        num, url, ia, who, boolean = obj
        if not boolean:
            f.write(url + "\n")
    f.write("\n")
    for obj in final_data:
        num, url, ia, who, boolean = obj
        if not boolean:
            f.write("- " + url + "\n")
            f.write("   - Earliest date found in Wayback Machine: " + ia + "\n")
            f.write("   - Creation date according to WHOIS lookup: " + who + "\n")
