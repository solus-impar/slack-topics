"""topics.callables module: plugins for slack-topics.

Below is some of the requirements for plugins.

Args:
    None

Returns:
    topic, massage, channel (tuple of strings): `topic` for `channel` with
        a `message` posted to `channel`. `message` is typically a link
        for `topic`. `message` and `channel` can be empty.

Raises:
    Not required, but use when needed.
"""
import random
import re
from typing import Tuple
from slack_topics.topics.utils import fetch_json, topic, url_to_soup


@topic
def random_man_page() -> Tuple[str, str, str]:
    """Randomly select a man page from Ubuntu manuals."""
    sec = random.randrange(1, 9)
    man_url = "http://manpages.ubuntu.com/manpages/xenial/man{}/".format(sec)
    man_soup = url_to_soup(man_url)
    man_page = random.choice(man_soup.find_all('a'))['href']
    link = "{}{}".format(man_url, man_page)
    for relation in [['.', '('], ['.', ')'], ['html', '']]:
        man_page = man_page.replace(relation[0], relation[1], 1)

    return man_page, link, ''


@topic
def random_programming_language() -> Tuple[str, str, str]:
    """Randomly select a programming language from Wikipedia."""
    wiki_url = 'https://en.wikipedia.org/wiki/List_of_programming_languages'
    wiki_soup = url_to_soup(wiki_url)
    lang_list = wiki_soup.find_all('div', class_='div-col columns column-width')
    lang_sublist = []
    for link in random.choice(lang_list).find_all('a', href=True):
        lang_sublist.append(link)
    lang = random.choice(lang_sublist)
    lang_url = "https://en.wikipedia.org{}".format(lang['href'])

    return lang['title'], lang_url, ''


@topic
def top_hacker_news_story() -> Tuple[str, str, str]:
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
def random_xkcd() -> Tuple[str, str, str]:
    """Select a random xkcd comic"""
    xkcd = 'https://xkcd.com'
    current = fetch_json("{}/info.0.json".format(xkcd))
    num = random.choice(range(1, current['num'] + 1))
    comic = fetch_json("{}/{}/info.0.json".format(xkcd, num))
    url = "{}/{}/".format(xkcd, num)

    return comic['safe_title'], url, 'random'


@topic
def random_cmd_challenge() -> Tuple[str, str, str]:
    """Randomly select a challenge from cmdchallenge.com."""
    cmd_url = "https://cmdchallenge.com/{}"
    cmd_json = fetch_json(cmd_url.format('challenges/challenges.json'))
    cmd_num = random.randrange(0, 29)
    cmd_name = cmd_json[cmd_num]['slug']
    link = cmd_url.format("#/{}".format(cmd_name))

    return cmd_name, link, ''


@topic
def trending_on_github() -> Tuple[str, str, str]:
    """Select the current trending repository this week on GitHub."""
    hub_url = 'https://github.com/trending?since=weekly'
    hub_soup = url_to_soup(hub_url)
    repo_list = hub_soup.find('ol', class_='repo-list')
    repo = repo_list.find('a')['href']
    link = "https://github.com{}".format(repo)

    return repo[1:], link, ''


@topic
def random_hackerrank_challenge() -> Tuple[str, str, str]:
    """Randomly select a challenge from hackerrank.com."""
    rank_url = 'https://hackerrank.com/dashboard'
    rank_soup = url_to_soup(rank_url)
    domains = []
    for link in rank_soup.find_all('a', \
        href=re.compile(r'/domains/(?!tutorials)')):
        domains.append(link['href'])

    domain_url = "https://hackerrank.com{}".format(random.choice(domains))
    domain_soup = url_to_soup(domain_url)

    subdomain_list = domain_soup.find('ul', id='challengeAccordion')
    subdomains = [link['href'] for link in subdomain_list.find_all('a')]

    challenges_url = "https://hackerrank.com{}".format( \
        random.choice(subdomains))
    challenges_soup = url_to_soup(challenges_url)
    challenges = []
    for link in challenges_soup.find_all('a', href=re.compile(r'/challenges/' \
        '(?!.*forum$|.*leaderboard$|.*submissions$)')):
        challenges.append(link)

    challenge = random.choice(challenges)
    challenge_url = "https://hackerrank.com{}".format(challenge['href'])

    return challenge.text, challenge_url, ''
