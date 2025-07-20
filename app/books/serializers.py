import logging
from rest_framework import serializers

from .models import Author, Book, Genre
from .validators import ISBNValidator

logger = logging.getLogger("library")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ("is_cancelled",)

    def to_representation(self, instance):
        logger.debug(f"Сериализация автора: {instance}")
        return super().to_representation(instance)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

    def to_representation(self, instance):
        logger.debug(f"Сериализация жанра: {instance}")
        return super().to_representation(instance)


class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(validators=[ISBNValidator.validate_isbn])
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"

    def to_representation(self, instance):
        logger.debug(f"Сериализация книги: {instance}")
        return super().to_representation(instance)

    def validate(self, data):
        logger.debug(f"Валидация книги: {data}")
        return super().validate(data)
