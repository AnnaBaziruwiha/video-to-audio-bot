import pytest


def test_is_youtube_link_valid(bot_instance):
    url = "http://www.youtube.com/watch?v=TestVideoID"
    assert (
        bot_instance._is_youtube_link(url) is True
    ), f"Expected True for {url}, but got False"


def test_is_youtube_link_invalid(bot_instance):
    url = "http://www.example.com/watch?v=TestVideoID"
    assert (
        bot_instance._is_youtube_link(url) is False
    ), f"Expected False for {url}, but got True"


def test_is_youtube_link_empty(bot_instance):
    assert (
        bot_instance._is_youtube_link("") is False
    ), f"Expected False for empty string, but got True"
