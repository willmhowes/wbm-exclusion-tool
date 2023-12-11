# Order of scripts

1. Generate YAML list of urls in `urls.yml`
1. Run `download_ia.py`
1. Run `download_whois.py`
1. Run `compare_urls.py`
1. If given list of csvs to compare, run `compare_csv.py`
1. Run `generate_final_report.py` in order to make internal note
1. Run `generate_exclusion_txt.py` in order to fill out exclusion report
