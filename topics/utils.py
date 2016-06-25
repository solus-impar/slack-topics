import sys
import requests


def topic(func):
    name = " ".join(w.title() for w in func.__name__.split('_'))
    func.__topic__ = name
    return func


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
