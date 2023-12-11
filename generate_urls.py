import os
import re


def generate_urls(txt: str, strip_www=False):
    """function that converts block of txt into list of urls"""
    urls: list = []
    regx = r"(?:https:\/\/|http:\/\/)?([a-zA-Z0-9\-]{2,}(?:\.[a-zA-Z0-9\-]{2,})*(?:\.[a-zA-Z\-]{2,}))"
    if strip_www:
        regx = r"(?:https:\/\/www\.|http:\/\/www\.|www.|https:\/\/|http:\/\/)?([a-zA-Z0-9\-]{2,}(?:\.[a-zA-Z0-9\-]{2,})*(?:\.[a-zA-Z\-]{2,}))"
    url_regex = re.compile(regx)
    candidate_urls = re.findall(url_regex, txt)
    urls = candidate_urls
    return urls
