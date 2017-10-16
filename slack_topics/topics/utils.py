"""slack-topics: utilities for fetching topics."""
import re
import sys
import requests
from bs4 import BeautifulSoup


def fetch_json(url):
    """Fetch data from a URL and attempt to parse it as JSON."""
    try:
        response = requests.get(url)
    except requests.ConnectionError:
        sys.exit("tb2k: error: cannot connect to {}".format(url))

    status_code = response.status_code
    if status_code == 200:
        try:
            return response.json()
        except ValueError:
            sys.exit("tb2k: error: invalid JSON at {}".format(url))
    else:
        sys.exit("tb2k: error: {} fetching {}".format(status_code, url))


def topic(c):
    """Identify a callable as a topic."""
    c.__topic__ = " ".join(w.title() for w in uncamel(c.__name__).split('_'))
    return c() if type(c) is type else c


def uncamel(s):
    """
    Convert CamelCase class names into lower_snake_case.
    Taken from http://stackoverflow.com/a/1176023/3288364
    """
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def url_to_soup(url):
    """url -> soup"""
    html = requests.get(url)
    return BeautifulSoup(html.text, 'html.parser')
