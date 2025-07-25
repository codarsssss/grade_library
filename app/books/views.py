import logging

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView
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

    def get_queryset(self):
        q = self.request.GET
        logger.debug(f"Параметры фильтрации: {q.dict()}")

        queryset = (
            Book.objects.select_related("author").prefetch_related("genres").all()
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

        self.full_queryset = queryset.distinct()

        try:
            page = int(q.get("page", 1))
            page_size = int(q.get("page_size", 12))
        except ValueError:
            page, page_size = 1, 12

        self.page = page
        self.page_size = page_size
        self.total_items = self.full_queryset.count()
        self.total_pages = (self.total_items + page_size - 1) // page_size

        start = (page - 1) * page_size
        end = start + page_size
        return self.full_queryset[start:end]

    def pagination_range(self):
        for page_number in range(1, self.total_pages + 1):
            yield page_number

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        context["authors"] = Author.objects.all()
        context["current_query"] = self.request.GET.get("query", "")
        context["page"] = self.page
        context["page_size"] = self.page_size
        context["total_items"] = self.total_items
        context["total_pages"] = self.total_pages
        context["has_next"] = self.page < self.total_pages
        context["has_previous"] = self.page > 1
        context["current_genre"] = self.request.GET.get("genre", "")
        context["current_author"] = self.request.GET.get("author", "")
        context["date_from"] = self.request.GET.get("date_from", "")
        context["date_to"] = self.request.GET.get("date_to", "")
        context["page_range"] = self.pagination_range()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            logger.debug("AJAX-запрос на фильтрацию книг")
            html = render_to_string(
                "books/includes/_book_list.html", context, request=self.request
            )
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
