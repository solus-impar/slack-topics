# Contributing to `tb2k`

`tb2k` keeps plugins in the [`topics.functions`][topic functions] module. If
you'd like to contribute a topic source of your own you can submit a pull
request to this repository adding a function to that module. Topic functions
**MUST** conform to the following specification:

1. Be decorated with the `@topic` decorator from [`topics.utils`][topic utils].
2. Take no arguments.
3. Return a `topic` string and a `link` string as a tuple.
  - The `link` _can_ be the empty string.

An example topic function might look like this:
```python
@topic
def wwu_cs_rules():
    topic = 'WWU CS is the best!'
    link = 'https://wwucs.slack.com'
    return topic, link
```

## Note
The `@topic` decorator sets a special attribute, `__topic__`, on the topic
function to signal that it is a topic, but also for naming purposes. The
`__topic__` attribute is used to provide source for links. For example,
the above function would show up in a Slack message like
> WWU CS Rules: https://wwucs.slack.com

Therefore, it behooves contributors to pick descriptive names for new topic
functions.

[topic functions]: https://github.com/solus-impar/tb2k/blob/master/topics/functions.py
[topic utils]: https://github.com/solus-impar/tb2k/blob/master/topics/utils.py
