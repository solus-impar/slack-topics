import slack_topics.topics.callables as tc


def test_topic_callables():
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

    topic_callables = []
    for attr in (getattr(tc, a) for a in dir(tc)):
        if callable(attr) and hasattr(attr, '__topic__'):
            topic_callables.append(attr)
    for topic_callable in topic_callables:
        topic, message, channel = topic_callable()
        assert isinstance(topic, str)
        assert isinstance(message, str)
        assert isinstance(channel, str)
        assert topic != ''
