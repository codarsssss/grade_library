from django.db import models

from .managers import AuthorManager, BookManager


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True, help_text="Отчество (если есть)")
    last_name = models.CharField(max_length=100, db_index=True)
    birth_date = models.DateField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False, help_text="Автор отменен")

    objects = AuthorManager()

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, help_text="10 или 13-значный номер ISBN", db_index=True)
    cover_image = models.ImageField(upload_to="book_covers/", null=True, blank=True)

    objects = BookManager()

    class Meta:
        ordering = ['-publication_date']
        indexes = [
            models.Index(fields=['author', 'publication_date']),
        ]

    def __str__(self):
        return f"{self.title} ({self.author.last_name})"
