# books/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Book, Author, Genre


class BookSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Book.objects.all()

    def lastmod(self, obj):
        return obj.publication_date

    def location(self, obj):
        return reverse("book_detail", args=[obj.pk])


class AuthorSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Author.objects.all()

    def location(self, obj):
        return reverse("author_detail", args=[obj.pk])


class GenreSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Genre.objects.all()

    def location(self, obj):
        return reverse("genre_detail", args=[obj.pk])
