# `tb2k`

A python3 slack topic bot.

## Dependencies

```
pip install --upgrade pip
pip install requests slackclient wikipedia
```

## Installation

```
git clone git@gitlab.cs.wwu.edu:canoym/tb2k.git
```
Run `setup.py` to create the cron job (uses `which` and `pwd`).
```
cd tb2k
python3 setup.py
```
Or, if you want to edit `crontab` yourself.
```
crontab -e
0 6 * * * \path\to\python3 \path\to\tb2k.py
```
Add your `token` and `channel` to `config.py`.
```
token = "TOKEN"
channel = "CHANNEL"
```
## Schedule
Every day at 06:00, `tb2k` will update the channel's topic
to one of thse pages.
* Monday, Tuesday, & Wednesday: Random man-page
* Thursday & Friday: Random Wikipedia page
* Saturday & Sunday: Top HN story

Slack API: [api.slack.com](//api.slack.com/)

You should also check out [wb2k](http://www.github.com/reillysiemens/wb2k/).

