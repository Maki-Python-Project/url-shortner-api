from celery import shared_task

from .utils import send


@shared_task
def send_a_message_to_email(user_email: str, shorturl: str, longurl: str) -> None:
    send(user_email, shorturl, longurl)
