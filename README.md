![GitHub workflow](https://github.com/AnnaBaziruwiha/video-to-audio-bot/actions/workflows/main.yml/badge.svg)

# Video to Audio Bot

This Telegram bot converts YouTube video links into audio files and sends them back to the user. It's designed to handle videos of any duration, and for audio files larger than 50MB (the Telegram limit), it splits them into multiple files.

## Technologies

This project is created with:

- [Python 3.10.10](https://www.python.org/downloads/release/python-31010/)
- [python-telegram-bot 20.3](https://python-telegram-bot.readthedocs.io/en/stable/)
- [youtube_dl 2022.3.25](https://github.com/ytdl-org/youtube-dl)
- [pydub 0.25.1](http://pydub.com/)
- [pytest 7.0.1](https://docs.pytest.org/en/latest/)
- [FFmpeg](https://ffmpeg.org/)

Please make sure to update tests as appropriate and keep these versions in mind when contributing.

## Setup and Installation

1. Clone this repository:

```bash
git clone https://github.com/AnnaBaziruwiha/video-to-audio-bot.git
```

2. Navigate to the project directory:

```bash
cd video-to-audio-bot
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. You also need to install FFmpeg or Libav to use pydub:

- For Ubuntu:

```bash
sudo apt-get install ffmpeg libavcodec-extra
```

- For Windows, download and extract FFmpeg or Libav from the official website.
- For MacOS:

```bash
brew install ffmpeg
```

5. Create a .env file and save `TELEGRAM_TOKEN` in it.

Start the bot:

```bash
python main.py
```

## Usage

Just send any YouTube link to the bot, and it will return an audio file of the video. If the audio file is larger than 50MB, it will be split into multiple files.

## Running Tests

To run the tests, use the following command:

```bash
pytest
```

## Contributing

Contributions are welcome! Please open an issue if you encounter any problems, or create a pull request if you want to add any new features.
