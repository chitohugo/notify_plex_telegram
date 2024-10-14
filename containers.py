import logging.config
import os

from celery import Celery
from dependency_injector import containers, providers
from plex_api_client import PlexAPI
from telegram import Bot
from watchdog.observers.polling import PollingObserver

from app.services.bot import TelegramBot
from app.services.detect_event_file import DetectEventFile
from app.services.plex_sdk import PlexSDK
from app.services.send_message import SendMessage


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(
        json_files=["./config.json"]
    )
    config.load()

    # Resources
    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    # Services
    base_path = providers.Callable(
        lambda:
        os.path.expanduser('~')
    )

    directory_name = providers.Callable(lambda: "Videos")
    path = providers.Callable(
        lambda:
        os.path.join(
            Container.base_path(),
            Container.directory_name()
        )
    )
    celery_service = providers.Singleton(
        Celery,
        'tasks',
        broker_url='redis://localhost:6379/0',
        include = ['app.tasks']
    )
    file_types = providers.Callable(lambda: ['.mp4', '.mkv', '.avi'])
    bot_service = providers.Factory(
        Bot,
        token=config.bot.token()
    )
    sdk_service = providers.Factory(
        PlexAPI,
        access_token=str(config.plex.access_token()),
        server_url=str(config.plex.server_url())
    )
    sdk_plex_service = providers.Factory(
        PlexSDK,
        s=sdk_service
    )
    telegram_service = providers.Factory(
        TelegramBot,
        bot=bot_service
    )
    send_message_service = providers.Factory(
        SendMessage
    )
    event_handler_service = providers.Factory(
        DetectEventFile,
        file_types=file_types,
        plex_service=sdk_plex_service,
        send_message=send_message_service
    )
    observer_service = providers.Singleton(PollingObserver)
