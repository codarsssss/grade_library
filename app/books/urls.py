from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthorViewSet,
    BookViewSet,
    GenreViewSet,
    BookListView,
    BookDetailView,
    AuthorDetailView,
    GenreDetailView
)

router = DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"books", BookViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", BookListView.as_view(), name="index"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre_detail'),
]
