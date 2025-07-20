import logging

from django.db import models

logger = logging.getLogger("library")


class AuthorManager(models.Manager):
    """
    Кастомный менеджер для авторов, возвращает только не отмененных авторов
    """

    def get_queryset(self):
        logger.debug("Выборка авторов: только неотмененные (is_cancelled=False)")
        return super().get_queryset().filter(is_cancelled=False)


class BookManager(models.Manager):
    """
    Кастомный менеджер для книг, исключает книги отмененных авторов
    """

    def get_queryset(self):
        logger.debug("Выборка книг: исключение книг отмененных авторов")
        return super().get_queryset().filter(author__is_cancelled=False)
