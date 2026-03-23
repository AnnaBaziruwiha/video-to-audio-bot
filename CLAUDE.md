# CLAUDE.md

## Project overview

Telegram bot that downloads YouTube videos as MP3 audio and sends them to the user. Handles large files by splitting at 50MB chunks.

## Running the bot

```bash
docker compose up -d           # start
docker compose logs -f bot     # tail logs
docker compose down            # stop
docker compose up -d --build   # rebuild after code changes
```

## Running tests

```bash
pytest
```

Tests live in `tests/unittests/`. All tests mock external dependencies (yt-dlp, pydub) — no network calls or real downloads.

## Architecture

Everything lives in `bot/bot.py` — a single `Bot` class that handles:
- Telegram polling and message handling (`handle_request`)
- YouTube audio download (`download_audio`) via yt-dlp
- Audio splitting for files >50MB (`split_audio`) via pydub
- Link extraction and validation (`extract_link`, `_is_youtube_link`)

Entry point is `main.py`, which reads `TELEGRAM_TOKEN` from `.env`.

Constants (messages, size limits) are in `utils/constants.py`.

## Key dependencies

- **yt-dlp** — YouTube downloader (replaces archived `youtube-dl`). Use `yt_dlp.YoutubeDL` with `noplaylist=True` to avoid playlist expansion.
- **pydub** — audio processing. Requires FFmpeg installed as a system dependency.
- **python-telegram-bot 20.x** — async Telegram API wrapper.

## Gotchas

- `outtmpl` in yt-dlp options must be set at init time (in the opts dict). Do **not** modify `ydl.params["outtmpl"]` after creation — yt-dlp treats `outtmpl` as a dict internally and will raise `TypeError: string indices must be integers`.
- YouTube URLs with `?list=` parameters will attempt playlist downloads unless `noplaylist=True` is set.
- The Docker volume `downloads/` persists audio files across restarts. The bot does not clean up files after sending — this is a known gap.
- Telegram has a 50MB file size limit. The `split_audio` method handles this by chunking into 10-minute segments.
