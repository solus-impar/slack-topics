# `slack-topics`

A python3 slack topic bot.

## Installation

```
pip3 install git+https://github.com/solus-impar/slack-topics.git@master
```

If you are not in a [virtualenv] you may need to use `pip3` with `sudo`.

## Usage
Once `slack-topics` is installed you can run it from the command line. Keep in mind
that `slack-topics` depends on the following environment variables:
* `TB2K_TOKEN`: A custom bot Slack token.
* `TB2K_CHANNEL`: The name of the channel to change topics for.

## Schedule
If you want `slack-topics` to run regularly you can add it to your `crontab` with
```
crontab -e
0 6  * * * slack-topics
0 14 * * * slack-topics
```

`slack-topics` will update a channel's topic to one of these pages.
* Random man-page
* Random programming language
* Top HN story
* Random xkcd comic

## New Topics
Don't like the topics that `slack-topics` currently supports? Follow the
[contribution guidelines] to add one!

## Resources
Slack API: [api.slack.com](https://api.slack.com/)

You should also check out [wb2k].

[wb2k]: https://www.github.com/reillysiemens/wb2k/
[virtualenv]: https://virtualenv.pypa.io/en/stable/
[contribution guidelines]: https://github.com/solus-impar/slack-topics/blob/master/CONTRIBUTING.md
