from csv import DictReader
import datetime

with open("domainsanddates.csv", "r") as f:
    dict_reader = DictReader(f)
    calculated_dates = list(dict_reader)

with open("given.csv", "r") as f:
    dict_reader = DictReader(f)
    given_dates = list(dict_reader)

for i, calc_entry in enumerate(calculated_dates):
    print(i+1, calc_entry["domain"])
    for given_entry in given_dates:
        if calc_entry["domain"] == given_entry["domain"]:
            calc_date = calc_entry["date"]
            calc_date = datetime.date.fromisoformat(calc_date)

            given_date = given_entry["date"]
            given_date_parts = given_date.split("/")
            given_date = datetime.date(
                int("20" + given_date_parts[2]),
                int(given_date_parts[0]),
                int(given_date_parts[1]),
            )

            if calc_date == given_date:
                print("Match")
