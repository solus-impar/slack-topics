import sys
import random
import wikipedia
from topics.utils import topic, fetch_json
import requests
from bs4 import BeautifulSoup


@topic
def random_man_page():
    """Randomly select a man page from Ubuntu manuals."""
    sec = random.randrange(1, 9)
    man_url = "http://manpages.ubuntu.com/manpages/xenial/man{}/".format(sec)
    man_html = requests.get(man_url)
    man_soup = BeautifulSoup(man_html.text, 'html.parser')
    
    man_page = random.choice(man_soup.find_all('a'))['href']
    link = "{}{}".format(man_url, man_page)

    for relation in [['.', '('], ['.', ')'], ['html', '']]:
        man_page = man_page.replace(relation[0], relation[1], 1)

    return man_page, link, ''


@topic
def random_wikipedia_programming_language():
    """Randomly select a programming language from Wikipedia."""
    title = 'List of programming languages'
    page = wikipedia.page(title=title)
    lang = random.choice(page.links)
    lang_url = "https://en.wikipedia.org/wiki/{}".format(lang.replace(' ', '_'))
    return lang, lang_url, ''


@topic
def top_hacker_news_story():
    """Select the current top Hacker News story."""
    hn_api = 'https://hacker-news.firebaseio.com/v0'
    hn_url = 'https://news.ycombinator.com'

    stories_url = "{}/topstories.json".format(hn_api)
    stories = fetch_json(stories_url)

    story_url = "{}/item/{}.json".format(hn_api, stories[0])
    story = fetch_json(story_url)
    discussion = "{}/item?id={}".format(hn_url, stories[0])
    message = "{}\nDiscussion: {}".format(story['url'], discussion)

    return story['title'], message, ''


@topic
def random_xkcd():
    """Select a random xkcd comic"""
    xkcd = "https://xkcd.com"
    current = fetch_json("{}/info.0.json".format(xkcd))
    num = random.choice(range(1, current['num'] + 1))
    comic = fetch_json("{}/{}/info.0.json".format(xkcd, num))
    url = "{}/{}/".format(xkcd, num)
    return comic['safe_title'], url, 'random'
