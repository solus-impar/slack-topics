# Contributing to `tb2k`

`tb2k` keeps plugins in the [`topics.callables`][topic callables] module. If
you'd like to contribute a topic source of your own you can submit a pull
request to this repository adding a callable object to that module. Topic
callables **MUST** conform to the following specification:

1. Be decorated with the `@topic` decorator from [`topics.utils`][topic utils].
2. Take no arguments.
3. Return a `topic` string, a `link` string, a `discussion` string, 
and a `channel` string as a tuple.
  - `link`, `discussion`,  and `channel` _can_ be the empty string.
  - If `channel` is an empty string, then it deaults to `TB2K_CHANNEL` if set
  or `general`.

An example topic function might look like this:
```python
@topic
def wwu_cs_rules():
    topic = 'WWU CS is the best!'
    link = 'https://wwucs.slack.com'
    channel = 'wwu'
    return topic, link, '', channel
```

An example topic class might look like this:
```python
@topic
class WesternWashingtonComputerScienceRules:
    def __init__(self):
        self.topic = 'WWU CS is the best!'
        self.link = 'https://wwucs.slack.com'
        self.discussion = ''
        self.channel = 'wwu'

    def __call__(self):
        return self.topic, self.link, self.discussion, self.channel
```

## Note
The `@topic` decorator sets a special attribute, `__topic__`, on the topic
function to signal that it is a topic, but also for naming purposes. The
`__topic__` attribute is used to provide source for links. For example,
the above function would show up in a Slack message like
> WWU CS Rules: https://wwucs.slack.com

and the above class would show up like
> Western Washington University Computer Science Rules: https://wwucs.slack.com

Therefore, it behooves contributors to pick descriptive names for new topic
callables.

[topic callables]: https://github.com/solus-impar/tb2k/blob/master/topics/callables.py
[topic utils]: https://github.com/solus-impar/tb2k/blob/master/topics/utils.py
