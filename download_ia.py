import os
import requests
import yaml
import json
import datetime
import streamlit as st


@st.cache_data
def download_iacdx(url):
    ia_request = f"https://web.archive.org/cdx/search/cdx?url={url}&fl=timestamp&output=json&limit=1"
    print("requesting", url)
    ia_response = requests.get(ia_request).json()
    return ia_response


def download_iacdx_bulk(urls):
    responses = []
    for i, url in enumerate(urls):
        ia_response = download_iacdx(url)
        ia_response["count"] = i + 1
        responses.append(ia_response)
    return responses


def download_iacdx_earliestdate(url):
    ia_response = download_iacdx(url)
    if len(ia_response) > 0:
        try:
            ia_earliest_date = ia_response[1][0]
            ia_earliest_date = (
                ia_earliest_date[0:4]
                + "-"
                + ia_earliest_date[4:6]
                + "-"
                + ia_earliest_date[6:8]
            )
            ia_earliest_date = datetime.date.fromisoformat(ia_earliest_date)
            ia_response = ia_earliest_date
        except ValueError:
            print("Error formatting creation date, returning raw value")
        return ia_response
    else:
        return "Unavailable"
