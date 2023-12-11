import os
import requests
import yaml
import json
import datetime
from dotenv import load_dotenv
import streamlit as st


@st.cache_data
def download_whois(url):
    load_dotenv()
    whois_request = f"https://whoisjsonapi.com/v1/{url}"
    print("requesting", url)
    whois_response = requests.get(
        whois_request, headers={"Authorization": "Bearer " + os.getenv("API_KEY")}
    ).json()
    return whois_response


def download_whois_bulk(urls):
    responses = []
    for i, url in enumerate(urls):
        whois_response = download_whois(url)
        whois_response["count"] = i + 1
        responses.append(whois_response)
    return responses


def download_whois_creationdate(url):
    whois_response = download_whois(url)
    whois_creation_date = whois_response["domain"]["created_date"]
    try:
        candidate_date = datetime.datetime.fromisoformat(whois_creation_date)
        candidate_date = candidate_date.date()
        whois_creation_date = candidate_date
    except ValueError:
        print("Error formatting creation date, returning raw value")
    return whois_creation_date
