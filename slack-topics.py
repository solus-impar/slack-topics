"""slack-topics: A python3 slack topic bot."""
import os
import sys
import random
import requests
from slackclient import SlackClient
import topics.callables as tc


def find_id(channel, bot):
    """Find the ID of a channel and whether it is public or private."""
    channels_list = bot.api_call("channels.list").get('channels')
    groups_list = bot.api_call("groups.list").get('groups')

    if not channels_list and not groups_list:
        sys.exit('slack-topics: error: couldn\'t enumerage channels/groups')

    # There is probably a better way to do this.
    channel_ids = [c['id'] for c in channels_list if c['name'] == channel]

    if channel_ids:
        return (channel_ids[0], 'channel')

    group_ids = [g['id'] for g in groups_list if g['name'] == channel]

    if group_ids:
        return (group_ids[0], 'group')
    else:
        sys.exit("slack-topics: error: couldn't find #{}".format(channel))


def main():
    """
    Set a channel topic to one of:
      - A random man-page
      - A random programming language from Wikipedia
      - The current top Hacker News story
    """

    token = os.environ.get('TB2K_TOKEN')
    channel = os.environ.get('TB2K_CHANNEL') or 'general'

    if not token:
        sys.exit('slack-topics: error: TB2K_TOKEN environment variable is not set')

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
        response = bot.api_call("{}s.setTopic".format(channel_type),
                                token=token, channel=channel_id, topic=topic)

        # The bot MUST be in the channel already. Bots cannot join channels.
        if not response['ok']:
            sys.exit("slack-topics: error: failed to set topic in #{}".format(channel))

        # Try to post link in channel.
        try:
            source = "{}: {}".format(topic_callable.__topic__, message)
            response = bot.api_call("chat.postMessage", token=token,
                                    channel=channel_id, text=source,
                                    as_user=True)
            if not response['ok']:
                sys.exit("slack-topics: error: failed to post link in #{}".format(
                    channel))
        except requests.ConnectionError:
            sys.exit("slack-topics: error: failed to connect to {}.".format(link))

if __name__ == "__main__":
    main()
