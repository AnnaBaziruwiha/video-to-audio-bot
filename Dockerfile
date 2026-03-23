FROM python:3.10-slim

# ffmpeg is required by pydub/youtube-dl for audio extraction
# git is required to install youtube-dl from the pinned git URL in requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p downloads

# Run as non-root user
RUN useradd --no-create-home appuser && chown -R appuser /app
USER appuser

CMD ["python", "main.py"]
