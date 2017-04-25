from unittest.mock import MagicMock

import pytest
import requests

from slack_topics.topics.utils import topic, uncamel, fetch_json


def test_topic_decorator_callable_class():
    """Test that classes can be decorated with @topic."""

    @topic
    class TestTopic:
        def __call__(self):
            return self.__topic__, 'message', '#general'

    assert TestTopic.__topic__ == 'Test Topic'


def test_topic_decorator_function():
    """Test that functions can be decorated with @topic."""

    @topic
    def test_topic():
        return 'Test Topic', 'message', '#general'

    assert test_topic.__topic__ == 'Test Topic'


@pytest.mark.parametrize('given,expected', (
    ('foobar', 'foobar'),
    ('FOOBAR', 'foobar'),
    ('Foobar', 'foobar'),
    ('fooBar', 'foo_bar'),
    ('FooBar', 'foo_bar'),
    ('FooBarBaz', 'foo_bar_baz'),
))
def test_uncamel(given, expected):
    """Test that camel case strings are converted to lower snake case."""
    assert uncamel(given) == expected


def test_fetch_json(monkeypatch):
    """Test fetch_json fetches valid JSON."""
    _json = dict(foo='bar')
    response = MagicMock(json=lambda: _json, status_code=200)
    _requests = MagicMock(get=lambda url: response)
    monkeypatch.setattr('slack_topics.topics.utils.requests', _requests)

    assert fetch_json('https://not.real/json') == _json


def test_fetch_json_exits_on_connection_error(monkeypatch):
    """Test fetch_json exists on requests.ConnectionError."""
    expected = 'tb2k: error: cannot connect to https://not.real/json'

    def _raise_connection_error(url):
        raise requests.ConnectionError

    monkeypatch.setattr('slack_topics.topics.utils.requests.get',
                        _raise_connection_error)

    with pytest.raises(SystemExit) as err:
        fetch_json('https://not.real/json')
    assert str(err.value) == expected


def test_fetch_json_exits_with_invalid_JSON(monkeypatch):
    """Test fetch_json exists if a response contains invalid JSON."""
    expected = 'tb2k: error: invalid JSON at https://not.real/json'

    def _raise_value_error():
        raise ValueError

    response = MagicMock(json=_raise_value_error, status_code=200)
    _requests = MagicMock(get=lambda url: response)
    monkeypatch.setattr('slack_topics.topics.utils.requests', _requests)

    with pytest.raises(SystemExit) as err:
        fetch_json('https://not.real/json')
    assert str(err.value) == expected


def test_fetch_json_exits_if_HTTP_status_not_200(monkeypatch):
    """Test fetch_json exits if a response status code is not 200."""
    expected = 'tb2k: error: 404 fetching https://not.real/json'

    response = MagicMock(status_code=404)
    _requests = MagicMock(get=lambda url: response)
    monkeypatch.setattr('slack_topics.topics.utils.requests', _requests)

    with pytest.raises(SystemExit) as err:
        fetch_json('https://not.real/json')
    assert str(err.value) == expected
