from unittest.mock import Mock, patch
import pytest
from bot.bot import Bot


def test_is_youtube_link():
    bot = Bot(Mock())

    assert bot.is_youtube_link("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert bot.is_youtube_link("https://youtu.be/dQw4w9WgXcQ")
    assert not bot.is_youtube_link("https://www.google.com")


@patch("bot.bot.Bot.process_youtube_link", return_value=["mocked_path"])
@patch("bot.bot.Bot.send_audio")
@patch("bot.bot.Bot.send_invalid_input_message")
def test_handle_message(
    mocked_invalid_input, mocked_send_audio, mocked_process, m_update, m_context
):
    bot = Bot(Mock(), Mock(), Mock())
    bot.handle_message(m_update, m_context)

    mocked_process.assert_called_once_with(m_update.message.text)
    mocked_send_audio.assert_called_once_with(m_update, m_context, "mocked_path")
    mocked_invalid_input.assert_not_called()
