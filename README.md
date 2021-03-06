# slack-topics
[![Build Status][badge-build]](https://travis-ci.org/solus-impar/slack-topics)

A python slack bot for topics.

## Installation

```
pip3 install git+https://github.com/solus-impar/slack-topics.git@master
```

If you are not in a [virtualenv] you may need to use `pip3` with `sudo` or
`--user`.

## Usage
Once `slack-topics` is installed you can run it from the command line. Keep in
mind that `slack-topics` depends on the following environment variables:
* `SLACK_TOPICS_TOKEN`: A custom bot Slack token.
* `SLACK_TOPICS_CHANNEL`: The name of the channel to change topics for.

## Schedule
If you want `slack-topics` to run regularly you can add it to your `crontab` or
`launchd`.

`slack-topics` will update a channel's topic to one of these pages.
* Random man-page
* Random programming language
* Top HN story
* Random xkcd comic
* Random challenge from [cmdchallenge.com]
* Top trending repository on Github
* Random HackerRank challenge

## New Topics
Don't like the topics that `slack-topics` currently supports? Follow the
[contribution guidelines] to add one!

## Resources
Slack API: [api.slack.com](https://api.slack.com/)

You should also check out [wb2k].

[badge-build]: https://travis-ci.org/solus-impar/slack-topics.svg?branch=master
[cmdchallenge.com]: https://cmdchallenge.com/
[wb2k]: https://www.github.com/reillysiemens/wb2k/
[virtualenv]: https://virtualenv.pypa.io/en/stable/
[contribution guidelines]: https://github.com/solus-impar/slack-topics/blob/master/CONTRIBUTING.md
