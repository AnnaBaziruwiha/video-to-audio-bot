import logging
import os
from dotenv import load_dotenv

from bot import Bot

load_dotenv()
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN", "")
    bot = Bot(token=token)
    bot.start()
