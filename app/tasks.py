import asyncio

from celery import Task
from dependency_injector.wiring import inject, Provide

from app.services.base_service import BaseService
from app.services.bot import TelegramBotAbstract
# from app.services.send_message import SendMessage
from containers import Container


# def send_message(self, template: str, photo_path: str):
#     try:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         loop.run_until_complete(
#             self.celery.register_task(
#                 self.send_message_to_channel(template, photo_path)
#             )
#         )
#     finally:
#         loop.close()
class TaskSend(Task, BaseService):
    def __init__(self):
        super().__init__()

    @inject
    def run(
            self,
            template: str,
            photo_path: str,
            bot: TelegramBotAbstract = Provide[Container.telegram_service]
    ):
        self.logger.info("Executing task send notification")
        if bot is None:
            self.logger("The bot could not be injected correctly.")

        try:
            self._send_notification(template, photo_path, bot)
        except Exception as e:
            self.logger.error(f"Error executing task: {e}")

    async def _send_notification(self, template: str, photo_path: str, bot: TelegramBotAbstract):
        await bot.send_message_to_channel(template, photo_path)

# send_notification = TaskSend()

# container = Container()
# container.init_resources()
# container.wire(modules=[__name__])
# celery = container.celery_service()
# telegram_bot = container.telegram_service()
#
# send_notification = TaskSend()
# celery.register_task(send_notification)
# data = {
#    "title":"Revolver",
#    "type":"movie",
#    "year":2024,
#    "studio":"Sanai Pictures",
#    "description":"Su-young, a police detective who went to prison for someone else, is surprised when a mysterious woman named Yoon-sun arrives to collect her on her day of release. As she discovers that the promised compensation for her time behind bars has vanished, Su-young embarks on a mission to reclaim what rightfully belongs to her.",
#    "library_section_uuid":"2697be8b-bfd1-49f2-b30f-93b3d15a7dbb",
#    "thumb_image":"/library/metadata/742/thumb/1728864627",
#    "thumb_image_url":"https://helpful-absolutely-rooster.ngrok-free.app/library/metadata/742/thumb/1728864627?X-Plex-Token=y6zdfpYG3QP9crx4Dyid",
#    "art":"/library/metadata/742/art/1728864627",
#    "media":[
#       {
#          "video_resolution":1080,
#          "audio_codec":"aac",
#          "bitrate":2384,
#          "duration":6869653,
#          "parts":[
#             {
#                "file":"/home/hugogonzalez/Videos/Movies/Revolver (2024) [1080p] [WEBRip] [YTS.MX]/Revolver.2024.1080p.WEBRip.x264.AAC-[YTS.MX].mp4",
#                "size":2047544976,
#                "container":"mp4"
#             }
#          ]
#       }
#    ],
#    "rating_key":742,
#    "movie_url":"https://helpful-absolutely-rooster.ngrok-free.app/web/index.html#!/server/f78f368c57a8324fb9d374ddb5c185ba2afebfc6/details?key=/library/metadata/742"
# }
# send = SendMessage()
# send.process_event(data)
# image_url = " https://helpful-absolutely-rooster.ngrok-free.app/library/metadata/727/thumb/1728847523?X-Plex-Token=y6zdfpYG3QP9crx4Dyid"
# send_notification.apply_async(args=(data, image_url))
