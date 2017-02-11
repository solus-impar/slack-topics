import os
import sys
import random
import requests
from slackclient import SlackClient
import topics.callables as tc


def find_id(channel, bot):
    """Find the ID of a channel and whether it is public or private.

    Args:
        channel (string): Name of channel, i.e. `general`.
        bot (SlackClient): Slack-bot for API calls.

    Returns:
        channel_id, channel_type (tuple of strings): `channel_id` for API
            calls when you can't use just `channel`. `channel_type` can be
            'channel' or 'group'.

    Raises:
        ValueError
    """

    channels_list = bot.api_call("channels.list").get('channels')
    groups_list = bot.api_call("groups.list").get('groups')

    assert channels_list
    assert groups_list

    # There is probably a better way to do this.
    channel_ids = [c['id'] for c in channels_list if c['name'] == channel]

    if channel_ids:
        return channel_ids[0], 'channel'

    group_ids = [g['id'] for g in groups_list if g['name'] == channel]

    if group_ids:
        return group_ids[0], 'group'
    else:
        raise ValueError


def test_slack_bot():
    """Set a channel topic to one of:
        - A random man-page
        - A random programming language from Wikipedia
        - The current top Hacker News story
        - Random xkcd comic
        - Random challenge from cmdchallenge.com

    Args:
        None

    Returns:
        None

    Raises:
        ConnectionError
    """

    token = os.environ.get('SLACK_TOPICS_TOKEN')
    channel = os.environ.get('SLACK_TOPICS_CHANNEL') or 'general'

    assert token

    bot = SlackClient(token)
    if bot.rtm_connect():

        topic_callables = []
        for attr in (getattr(tc, a) for a in dir(tc)):
            if callable(attr) and hasattr(attr, '__topic__'):
                topic_callables.append(attr)
        topic_callable = random.choice(topic_callables)
        topic, message, topic_channel = topic_callable()
        if topic_channel:
            channel = topic_channel

        channel_id, channel_type = find_id(channel, bot)

        # Try to set the channel topic.
        response = bot.api_call(
            "{}s.setTopic".format(channel_type),
            token=token,
            channel=channel_id,
            topic=topic
        )

        # The bot MUST be in the channel already. Bots cannot join channels.
        assert response['ok']

        # Try to post link in channel.
        try:
            source = "{}: {}".format(topic_callable.__topic__, message)
            response = bot.api_call(
                "chat.postMessage",
                token=token,
                channel=channel_id,
                text=source,
                as_user=True
            )
            assert response['ok']

        except:
            raise requests.ConnectionError

if __name__ == "__main__":
    main()
