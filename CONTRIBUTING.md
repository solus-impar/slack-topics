# Contributing to `tb2k`

`tb2k` keeps plugins in the [`topics.functions`][topic functions] module. If
you'd like to contribute a topic source of your own you can submit a pull
request to this repository adding a function to that module. Topic functions
**MUST** conform to the following specification:

1. Begin with the `topic_` prefix.
2. Take no arguments.
3. Return a `topic` string and a `link` string as a tuple.
  - The `link` _can_ be the empty string.

An example topic function might look like this:
```python
def topic_wwucs():
    topic = 'WWU CS rules!'
    link = 'https://wwucs.slack.com'
    return topic, link
```

[topic functions]: https://github.com/solus-impar/tb2k/blob/master/topics/functions.py
