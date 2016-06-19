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
            sec = str(random.randrange(1, 9))
            man_dir = "/usr/share/man/man" + sec + "/"
            page = random.choice(os.listdir(man_dir))
            page = page.split(".")
            topic = page[0] + "(" + sec + ")"
        # Thur Fri
        elif day < 5:
            # Random Wikipedia page
            topic = wikipedia.random(pages=1)
        # Sat Sun
        else:
            # Top HN story
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(url)
            data = response.json()
            url = "https://hacker-news.firebaseio.com/v0/item/"
            url += str(data[0]) + ".json"
            response = requests.get(url)
            data = response.json()
            topic = data['title']
        # Add print() to see response in /var/mail/$user
        bot.api_call("channels.setTopic", token=token,
                     channel=channel, topic=topic)


if __name__ == "__main__":
    main()
