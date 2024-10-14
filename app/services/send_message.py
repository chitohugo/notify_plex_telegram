from abc import abstractmethod, ABC

from app.services.base_service import BaseService


class SendMessageAbstract(ABC):
    @abstractmethod
    def send_message(self, template, image_url):
        pass

    @abstractmethod
    def process_event(self, data):
        pass

    @abstractmethod
    def set_template(self, movie):
        pass


class SendMessage(SendMessageAbstract, BaseService, ):
    def __init__(self):
        super().__init__()

    def send_message(self, template, image_url) -> None:
        self.logger.info(f'Sending message to {image_url}')
        from app.tasks import TaskSend
        send_notification = TaskSend()
        send_notification.apply_async(
            args=(template, image_url)
        )

    def process_event(self, data):
        self.logger.info(f'Received event from {data}')
        html_message = self.set_template(data)
        self.send_message(html_message, data["thumb_image_url"])

    def set_template(self, movie):
        self.logger.info(f'Setting template to {movie}')
        markdown_message = f"""
        *🎬 Nueva Película Agregada\\! 🎬*

        ¡Hola amigos\\! 
        Acabo de agregar una nueva película:
        
        *\\- Título:* _{movie['title']}_
        *\\- Año:* {movie['year']}
        *\\- Calidad:* {movie['media'][0]['video_resolution']}
        
        ¡Espero que la disfruten\\! 🍿
        
        [Link de la película]({movie["movie_url"]})
        """
        return markdown_message
