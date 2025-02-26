from rest_framework import serializers

from .models import Author, Genre, Book
from .validators import ISBNValidator


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        exclude = ('is_cancelled',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(validators=[ISBNValidator.validate_isbn])
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'
