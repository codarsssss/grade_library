from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_new_book_email(title):
    send_mail(
        subject=f"Новая книга: {title}",
        message=f"Добавлена новая книга: {title}",
        from_email="no-reply@library.local",
        recipient_list=["admin@library.local"],
    )
