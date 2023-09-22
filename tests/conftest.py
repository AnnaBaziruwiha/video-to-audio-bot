import pytest
from telegram import Update
from telegram.ext import CallbackContext

from bot import Bot


@pytest.fixture
def bot_instance():
    return Bot()


@pytest.fixture
def mock_telegram_context(mocker):
    return mocker.MagicMock(spec=CallbackContext)


@pytest.fixture
def mock_telegram_update(mocker):
    return mocker.MagicMock(spec=Update)


@pytest.fixture
def mock_youtube_dl(mocker):
    return mocker.patch("bot.bot.youtube_dl", autospec=True)


@pytest.fixture
def mock_os(mocker):
    return mocker.patch("bot.bot.os", autospec=True)


@pytest.fixture
def mock_audio_segment(mocker):
    return mocker.patch("bot.bot.AudioSegment", autospec=True)
