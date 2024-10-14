import logging

from dependency_injector.wiring import inject, Provide
from watchdog.observers import Observer

from app.services.detect_event_file import DetectEventFile
from app.tasks import TaskSend
from containers import Container


@inject
def main(
        path: str = Provide[Container.path],
        file_types: list = Provide[Container.file_types],
        event_handler: DetectEventFile = Provide[Container.event_handler_service],
        observer: Observer = Provide[Container.observer_service]
):

    # Initialize observer
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    logging.info(f"Monitoring the directory: {path} for file types {file_types}")


    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

container = Container()
container.init_resources()
container.wire(modules=[__name__])

celery = container.celery_service()

# Register tasks in Celery
send_notification = TaskSend()
celery.register_task(send_notification)

main()
