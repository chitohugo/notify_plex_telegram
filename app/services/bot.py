from abc import ABC, abstractmethod

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

from app.services.base_service import BaseService

CHANNEL_ID = '-1002263251738'


class TelegramBotAbstract(ABC):
    @abstractmethod
    async def send_message_to_channel(self, template, image_url: str = None):
        pass


class TelegramBot(TelegramBotAbstract, BaseService):
    def __init__(self, bot: Bot):
        self.bot = bot
        super().__init__()

    async def send_message_to_channel(self, template, image_url: str = None) -> None:
        self.logger.info(f"Photo url: {image_url}")
        try:
            await self.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=image_url,
                caption=template,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            self.logger.info(f"Message sent to channel: {template}")
        except TelegramError as e:
            self.logger.error(f"Error sending message to channel: {e}")
