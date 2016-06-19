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


def find_id(channel, bot):
    """Find the ID of a channel and whether it is public or private."""
    channels_list = bot.api_call("channels.list").get('channels')
    groups_list = bot.api_call("groups.list").get('groups')

    if not channels_list and not groups_list:
        sys.exit('tb2k: error: couldn\'t enumerage channels/groups')

    # There is probably a better way to do this.
    channel_ids = [c['id'] for c in channels_list if c['name'] == channel]

    if channel_ids:
        return (channel_ids[0], 'channel')

    group_ids = [g['id'] for g in groups_list if g['name'] == channel]

    if group_ids:
        return (group_ids[0], 'group')
    else:
        sys.exit("tb2k: error: couldn't find #{}".format(channel))


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


def man_page():
    """Randomly select a man page from /usr/share/man/."""
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

    return "{}({})".format(page.split('.')[0], sec)


def wikipedia_programming_language():
    """Randomly select a programming language from Wikipedia."""
    title = 'List of programming languages'
    page = wikipedia.WikipediaPage(title=title)
    return random.choice(page.links)


def top_hacker_news_story():
    """Select the current top Hacker News story."""
    hn_api = 'https://hacker-news.firebaseio.com/v0'

    stories_url = "{}/topstories.json".format(hn_api)
    stories = fetch_json(stories_url)

    story_url = "{}/item/{}.json".format(hn_api, stories[0])
    story = fetch_json(story_url)

    return story['title']


def main():
    """
    Set a channel topic to one of:
      - A random man-page
      - A random programming language from Wikipedia
      - The current top Hacker News story
    """

    token = os.environ.get('TB2K_TOKEN')
    channel = os.environ.get('TB2K_CHANNEL') or 'general'

    if not token:
        sys.exit('tb2k: error: TB2K_TOKEN environment variable is not set')

    bot = SlackClient(token)
    if bot.rtm_connect():
        day = date.today().weekday()
        # Mon Tue Wed
        if day < 3:
            topic = man_page()
        # Thur Fri
        elif day < 5:
            topic = wikipedia_programming_language()
        # Sat Sun
        else:
            topic = top_hacker_news_story()

        channel_id, channel_type = find_id(channel, bot)

        # Try to set the channel topic.
        response = bot.api_call("{}s.setTopic".format(channel_type),
                                token=token, channel=channel_id, topic=topic)

        # The bot MUST be in the channel already. Bots cannot join channels.
        if not response['ok']:
            sys.exit("tb2k: error: failed to set topic in #{}".format(channel))


if __name__ == "__main__":
    main()
