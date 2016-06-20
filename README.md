# `tb2k`

A python3 slack topic bot.

## Installation

```
pip install git+https://gitlab.cs.wwu.edu/canoym/tb2k.git@master
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
0 6 * * * \path\to\python3 \path\to\tb2k.py
```

Every day at 06:00, `tb2k` will update the channel's topic
to one of thse pages.
* Monday, Tuesday, & Wednesday: Random man-page
* Thursday & Friday: Random Wikipedia page
* Saturday & Sunday: Top HN story

Slack API: [api.slack.com](https://api.slack.com/)

You should also check out [wb2k](http://www.github.com/reillysiemens/wb2k/).

[virtualenv]: https://virtualenv.pypa.io/en/stable/
