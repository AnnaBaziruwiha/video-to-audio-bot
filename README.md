![GitHub workflow](https://github.com/AnnaBaziruwiha/video-to-audio-bot/actions/workflows/main.yml/badge.svg)

# Video to Audio Bot

A Telegram bot that converts YouTube links into MP3 audio files and sends them back to the user. Handles videos of any duration — audio files larger than 50MB (Telegram's limit) are automatically split into multiple files.

## Technologies

- [Python 3.10](https://www.python.org/downloads/release/python-31012/)
- [python-telegram-bot 20.3](https://python-telegram-bot.readthedocs.io/en/stable/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — actively maintained YouTube download library
- [pydub 0.25.1](http://pydub.com/)
- [FFmpeg](https://ffmpeg.org/)
- [pytest 7.3](https://docs.pytest.org/en/latest/)
- [Docker](https://www.docker.com/)

## Running with Docker (recommended)

1. Clone the repo:

```bash
git clone https://github.com/AnnaBaziruwiha/video-to-audio-bot.git
cd video-to-audio-bot
```

2. Create a `.env` file with your Telegram bot token (get one from [@BotFather](https://t.me/BotFather)):

```bash
cp .env.example .env
# edit .env and set TELEGRAM_TOKEN
```

3. Start the bot:

```bash
docker compose up -d
```

4. View logs:

```bash
docker compose logs -f bot
```

## Running locally

1. Install FFmpeg:

```bash
# Ubuntu
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` with your token:

```bash
cp .env.example .env
# edit .env and set TELEGRAM_TOKEN
```

4. Start the bot:

```bash
python main.py
```

## Usage

Send any YouTube link to the bot. It will download the audio and send it back as an MP3. Links with playlist parameters (e.g. `?list=...`) are handled — only the single video is downloaded.

## Running Tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please open an issue if you encounter any problems, or create a pull request to add new features.
