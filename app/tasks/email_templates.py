from email.message import EmailMessage
from pydantic import EmailStr
from app.settings import settings


def create_booking_confirmation_template(
        email_to: str,
):
    email_message = EmailMessage()
    email_message['Subject'] = 'Подтверждение бронирования'
    email_message['From'] = settings.SMTP_USER
    email_message['To'] = email_to
    email_message.set_content(f"""
                <h1>Подтвердите бронирование</h1>
                Вы забронировали комнату
                """, subtype='html')

    return email_message
