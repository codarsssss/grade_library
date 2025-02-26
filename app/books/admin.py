from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Author, Book, Genre


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "middle_name", "birth_date", "is_cancelled")
    list_filter = ("is_cancelled",)
    search_fields = ("last_name", "first_name", "middle_name")
    ordering = ("last_name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_date", "isbn")
    list_filter = ("publication_date",)
    search_fields = ("title", "isbn")
    ordering = ("publication_date",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


admin.site.unregister(User)
admin.site.unregister(Group)
