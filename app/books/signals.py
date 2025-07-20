from django.db.models.signals import post_save
from django.dispatch import receiver
from books.models import Book
from .tasks import send_new_book_email as send_new_book_email_task


@receiver(post_save, sender=Book)
def send_new_book_email(sender, instance, created, **kwargs):
    if created:
        send_new_book_email_task.delay(instance.title)
