import celery
from pathlib import Path
from PIL import Image
from pydantic import EmailStr
from app.tasks.email_templates import create_booking_confirmation_template
import smtplib

from app.settings import settings
from app.tasks.celery_main import celery_app


@celery_app.task
def process_picture(path: str):
    im_path = Path(path)  # передаем путь до картинки
    im = Image.open(im_path)

    im_resized = im.resize((1000, 500))   # Делаем два размера
    im_avatar = im.resize((200, 100))

    im_resized.save(f'app/static/images/resized_1000_500_{im_path.name}')
    im_avatar.save(f'app/static/images/resized_200_100_{im_path.name}')


@celery_app.task()
def send_booking_confirmation(email: EmailStr):
    email = 'YegorMonahow@yandex.ru'
    msg_content = create_booking_confirmation_template(email_to=email)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg_content)
