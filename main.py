import logging

from bot import Bot

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if __name__ == "__main__":
    bot = Bot()
    bot.start()
