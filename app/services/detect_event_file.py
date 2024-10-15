import os

from watchdog.events import FileSystemEventHandler

from app.services.base_service import BaseService
from app.services.plex_sdk import PlexSDKAbstract
from app.services.send_message import SendMessageAbstract



class DetectEventFile(FileSystemEventHandler, BaseService):
    def __init__(self, file_types: list, plex_service: PlexSDKAbstract, send_message: SendMessageAbstract):
        self.file_types = file_types if file_types else []
        self.plex_service = plex_service
        self.send_message = send_message
        super().__init__()

    def process(self, event):
        self.logger.info(f"Processing event {event.event_type} in path {event.src_path}")
        _event = event.event_type
        _path = event.src_path
        extension = os.path.splitext(_path)[1]
        if _event in ['created'] and extension in self.file_types:
            self.logger.info(f"{_event} directory: {_path}".capitalize())
            info_movie = self.plex_service.get_last_added_movie()
            self.logger.info(f"Information movie: {info_movie}")
            self.send_message.process_event(info_movie)

        if self.file_types and not any(event.src_path.endswith(ext) for ext in self.file_types):
            return

    def on_created(self, event):
        self.process(event)

    # def on_modified(self, event):
    #     self.process(event)

    # def on_deleted(self, event):
    #     self.process(event)
