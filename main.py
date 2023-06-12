import os
from bot.bot import Bot
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    print("Retrieving token...")
    token = os.getenv("TELEGRAM_TOKEN")
    print("Initializing bot...")
    bot = Bot(token)
    print("Starting bot...")
    bot.start()
