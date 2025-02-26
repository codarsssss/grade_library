from django.db import models


class AuthorManager(models.Manager):
    """Кастомный менеджер для авторов, возвращает только не отмененных авторов"""
    def get_queryset(self):
        return super().get_queryset().filter(is_cancelled=False)


class BookManager(models.Manager):
    """Кастомный менеджер для книг, исключает книги отмененных авторов"""
    def get_queryset(self):
        return super().get_queryset().filter(author__is_cancelled=False)
