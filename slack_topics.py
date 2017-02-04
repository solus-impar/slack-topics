"""slack-topics: A python3 slack topic bot."""
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
        None
    """

    channels_list = bot.api_call("channels.list").get('channels')
    groups_list = bot.api_call("groups.list").get('groups')
    error = "slack-topics: error: {}"

    if not channels_list and not groups_list:
        sys.exit(error.format(
            'couldn\'t enumerage channels/groups'
        ))

    # There is probably a better way to do this.
    channel_ids = [c['id'] for c in channels_list if c['name'] == channel]

    if channel_ids:
        return channel_ids[0], 'channel'

    group_ids = [g['id'] for g in groups_list if g['name'] == channel]

    if group_ids:
        return group_ids[0], 'group'
    else:
        sys.exit(error.format(
            "couldn't find #{}".format(channel)
        ))


def main():
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
    error = "slack-topics: error: {}"

    if not token:
        sys.exit(error.format(
            'SLACK_TOPICS_TOKEN environment variable is not set'
        ))

    bot = SlackClient(token)
    if bot.rtm_connect():

        # Get all attributes in the topics.functions module that are callable
        # and possess the custom __topic__ attribute.
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
        if not response['ok']:
            sys.exit(error.format(
                "failed to set topic in #{}".format(channel)
            ))

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
            if not response['ok']:
                sys.exit(error.format(
                    "failed to post link in #{}".format(channel)
                ))
        except requests.ConnectionError:
            sys.exit(error.format(
                "failed to connect to {}.".format(message)
            ))

if __name__ == "__main__":
    main()
