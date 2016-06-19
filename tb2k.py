###
# tb2k: Slack Topic Bot
# Author: Mike Canoy (canoym@students.wwu.edu)
###

import sys
from slackclient import SlackClient
from datetime import date
import os
import random
import wikipedia
import requests


def main():

    token = os.environ.get('TB2K_TOKEN')
    channel = os.environ.get('TB2K_CHANNEL') or 'general'

    if not token:
        sys.exit('tb2k: error: TB2K_TOKEN environment variable is not set')

    bot = SlackClient(token)
    if bot.rtm_connect():
        day = date.today().weekday()
        # Mon Tue Wed
        if day < 3:
            # Random man-page
            sec = random.randrange(1, 9)
            man_dir = "/usr/share/man/man{}/".format(sec)

            try:
                page = random.choice(os.listdir(man_dir))
            except IndexError:
                sys.exit("tb2k: error: no man pages in section {}".format(sec))
            except FileNotFoundError:
                sys.exit("tb2k: error: {} does not exist".format(man_dir))
            except PermissionError:
                sys.exit("tb2k: error: {}: permission denied".format(man_dir))

            topic = "{}({})".format(page.split('.')[0], sec)
        # Thur Fri
        elif day < 5:
            # Random programming language from Wikipedia
            title = 'List of programming languages'
            page = wikipedia.WikipediaPage(title=title)
            topic = random.choice(page.links)
        # Sat Sun
        else:
            # Top HN story
            hn_api = 'https://hacker-news.firebaseio.com/v0'

            url = "{}/topstories.json".format(hn_api)

            try:
                response = requests.get(url)
            except requests.ConnectionError:
                sys.exit("tb2k: error: cannot connect to {}".format(url))

            status_code = response.status_code
            if status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    sys.exit("tb2k: error: invalid JSON at {}".format(url))
            else:
                sys.exit("tb2k: error: {} fetching {}".format(status_code, url))

            url = "{}/item/{}.json".format(hn_api, data[0])

            try:
                response = requests.get(url)
            except requests.ConnectionError:
                sys.exit("tb2k: error: cannot connect to {}".format(url))

            status_code = response.status_code
            if status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    sys.exit("tb2k: error: invalid JSON at {}".format(url))
            else:
                sys.exit("tb2k: error: {} fetching {}".format(status_code, url))

            topic = data['title']

        # Add print() to see response in /var/mail/$user
        bot.api_call("channels.setTopic", token=token,
                     channel=channel, topic=topic)


if __name__ == "__main__":
    main()
