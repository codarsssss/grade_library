import logging

from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.template.loader import render_to_string
from rest_framework import viewsets

from .models import Author, Book, Genre
from .serializers import AuthorSerializer, BookSerializer, GenreSerializer

logger = logging.getLogger("library")

# --- DRF ViewSets ---

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def list(self, request, *args, **kwargs):
        logger.info("Получен список авторов через API")
        return super().list(request, *args, **kwargs)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def list(self, request, *args, **kwargs):
        logger.info("Получен список жанров через API")
        return super().list(request, *args, **kwargs)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").prefetch_related("genres").all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        logger.info("Получен список книг через API")
        return super().list(request, *args, **kwargs)


# --- Классические Views ---

class BookListView(ListView):
    model = Book
    template_name = "books/index.html"
    context_object_name = "books"
    paginate_by = 12

    def get_queryset(self):
        q = self.request.GET
        logger.debug(f"Параметры фильтрации: {q.dict()}")

        queryset = (
            Book.objects.select_related("author")
            .prefetch_related("genres")
            .all()
        )

        try:
            if q.get("query"):
                queryset = queryset.filter(title__icontains=q["query"])
            if q.get("genre"):
                queryset = queryset.filter(genres__id=q["genre"])
            if q.get("author"):
                queryset = queryset.filter(author__id=q["author"])
            if q.get("date_from"):
                queryset = queryset.filter(publication_date__gte=q["date_from"])
            if q.get("date_to"):
                queryset = queryset.filter(publication_date__lte=q["date_to"])
        except Exception as e:
            logger.exception(f"Ошибка при фильтрации книг: {e}")

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["authors"] = Author.objects.all()
        context["current_query"] = self.request.GET.get("query", "")
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            logger.debug("AJAX-запрос на фильтрацию книг")
            html = render_to_string("books/includes/_book_list.html", context, request=self.request)
            return JsonResponse({"html": html})
        return super().render_to_response(context, **response_kwargs)


class BookDetailView(DetailView):
    model = Book
    template_name = "books/books/detail.html"
    context_object_name = "book"

    def get(self, request, *args, **kwargs):
        logger.info(f"Открытие деталки книги ID={kwargs.get('pk')}")
        return super().get(request, *args, **kwargs)


class AuthorDetailView(DetailView):
    model = Author
    template_name = "books/author/detail.html"
    context_object_name = "author"

    def get(self, request, *args, **kwargs):
        logger.info(f"Открытие деталки автора ID={kwargs.get('pk')}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context


class GenreDetailView(DetailView):
    model = Genre
    template_name = "books/genre/detail.html"
    context_object_name = "genre"

    def get(self, request, *args, **kwargs):
        logger.info(f"Открытие деталки жанра ID={kwargs.get('pk')}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context
