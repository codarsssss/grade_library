from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.template.loader import render_to_string
from rest_framework import viewsets

from .models import Author, Book, Genre
from .serializers import AuthorSerializer, BookSerializer, GenreSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").prefetch_related("genres").all()
    serializer_class = BookSerializer

class BookListView(ListView):
    model = Book
    template_name = "books/index.html"
    context_object_name = "books"
    paginate_by = 12  # опционально, если нужна пагинация

    def get_queryset(self):
        queryset = (
            Book.objects.select_related("author")
            .prefetch_related("genres")
            .all()
        )

        q  = self.request.GET
        query = q.get("query")
        genre_id = q.get("genre")
        author_id = q.get("author")
        date_from = q.get("date_from")
        date_to = q.get("date_to")

        if query:
            queryset = queryset.filter(title__icontains=query)

        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)

        if author_id:
            queryset = queryset.filter(author__id=author_id)

        if date_from:
            queryset = queryset.filter(publication_date__gte=date_from)

        if date_to:
            queryset = queryset.filter(publication_date__lte=date_to)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["authors"] = Author.objects.all()
        q = self.request.GET
        context.update({
            "current_query": q.get("query", ""),
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string("books/includes/_book_list.html", context, request=self.request)
            return JsonResponse({"html": html})
        return super().render_to_response(context, **response_kwargs)


class BookDetailView(DetailView):
    model = Book
    template_name = "books/books/detail.html"
    context_object_name = "book"


class AuthorDetailView(DetailView):
    model = Author
    template_name = "books/author/detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context


class GenreDetailView(DetailView):
    model = Genre
    template_name = "books/genre/detail.html"
    context_object_name = "genre"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context