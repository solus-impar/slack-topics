# `tb2k`

A python3 slack topic bot.

## Installation

```
pip install git+https://github.com/solus-impar/tb2k.git@master
```

If you are not in a [virtualenv] you may need to use `pip` with `sudo`.

## Usage
Once `tb2k` is installed you can run it from the command line. Keep in mind
that `tb2k` depends on the following environment variables:
- `TB2K_TOKEN`: A custom bot Slack token.
- `TB2K_CHANNEL`: The name of the channel to change topics for.

## Schedule
If you want `tb2k` to run regularly you can add it to your `crontab` with
```
crontab -e
0 6  * * * tb2k
0 14 * * * tb2k
```

Every day at 06:00 & 14:00, `tb2k` will update the channel's topic
to one of these pages.
* Random man-page
* Random programming language
* Top HN story
* Random xkcd comic

## New Topics
Don't like the topics that `tb2k` currently supports? Follow the
[contribution guidelines] to add one!

## Resources
Slack API: [api.slack.com](https://api.slack.com/)

You should also check out [wb2k].

[wb2k]: https://www.github.com/reillysiemens/wb2k/
[virtualenv]: https://virtualenv.pypa.io/en/stable/
[contribution guidelines]: https://github.com/solus-impar/tb2k/blob/master/CONTRIBUTING.md
