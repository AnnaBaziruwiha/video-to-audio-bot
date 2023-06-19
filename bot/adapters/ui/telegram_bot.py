import re
import os
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    CallbackContext,
    CommandHandler,
)
from dotenv import load_dotenv
from utils.constants import (
    WELCOME_MESSAGE,
    INVALID_INPUT_MESSAGE,
    RESPONSE_MESSAGE,
    RESPONSE_MESSAGE_ERROR,
)
from typing import Optional, Dict, Tuple
from dataclasses import dataclass

from .base import UserInterfaceClass

load_dotenv()


@dataclass
class BotState:
    """Stores the current state of the bot"""

    video_link: Optional[str] = None
    error: Optional[str] = None
    update: Optional[Update] = None
    context: Optional[CallbackContext] = None


class Bot(UserInterfaceClass):
    """Handles the communication with the Telegram bot"""

    def __init__(self):
        self.token: str = os.getenv("TELEGRAM_TOKEN", "")
        self.application: Application = Application.builder().token(self.token).build()
        self.persistent_data = BotState()

    def update_persistent_data(self, update: Update, context: CallbackContext) -> None:
        """Updates the persistent data"""
        self.persistent_data.update = update
        self.persistent_data.context = context

    def get_persistent_data(self) -> Tuple:
        """Returns the persistent data"""
        return self.persistent_data.context, self.persistent_data.update

    async def send_welcome_message(
        self, update: Update, context: CallbackContext
    ) -> None:
        """Sends a welcome message to the user"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=WELCOME_MESSAGE
        )

    def start(self) -> None:
        """Creates handlers for the bots, and starts polling"""
        start_handler = CommandHandler("start", self.send_welcome_message)
        message_handler = MessageHandler(
            filters.TEXT & (~filters.COMMAND), self.handle_request
        )
        self.application.add_handler(message_handler)
        self.application.add_handler(start_handler)
        self.application.run_polling(1.0)

    async def handle_request(self, additional_data: Dict[str, str]) -> None:
        """Function called when a user sends a message."""
        update = additional_data.get("update")
        context = additional_data.get("context")
        if not update or not context:
            print(
                f"The request doesn't contain update or context. Additional data: {additional_data}"
            )
            return
        message = update.message
        if message:
            self.update_persistent_data(update, context)
            return message

    async def return_success(self) -> None:
        """Returns a success message to the user"""
        context = self.persistent_data.context
        update = self.persistent_data.update
        if not context or not update:
            print("Update or context missing.")
            return
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=RESPONSE_MESSAGE
        )

    async def return_invalid_input(self) -> None:
        """Sends a message in response to an invalid request"""
        context = self.persistent_data.context
        update = self.persistent_data.update
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=INVALID_INPUT_MESSAGE
        )

    async def return_audio(self, audio_file: str) -> None:
        """Sends an audio file"""
        context = self.persistent_data.context
        update = self.persistent_data.update
        await context.bot.send_audio(
            chat_id=update.effective_chat.id, audio=open(audio_file, "rb")
        )
