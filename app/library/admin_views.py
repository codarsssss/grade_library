import csv

from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import redirect, render
from .forms import CSVImportForm
from books.models import Author, Book, Genre
from books.validators import ISBNValidator



class CSVImportAdminView:
    """Отдельная вью для импорта CSV в админке"""

    @staticmethod
    def get_urls():
        return [
            path("admin/import-csv/", CSVImportAdminView.view, name="admin_import_csv"),
        ]

    @staticmethod
    def view(request):
        if request.method == "POST":
            form = CSVImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data["csv_file"]
                decoded = csv_file.read().decode("utf-8").splitlines()
                reader = csv.DictReader(decoded)

                created = 0
                for row in reader:
                    try:
                        ISBNValidator.validate_isbn(row["isbn"])

                        author, _ = Author.objects.get_or_create(
                            first_name=row.get("first_name"),
                            last_name=row.get("last_name"),
                            middle_name=row.get("middle_name"),
                            birth_date=row.get("birth_date")
                        )

                        book, book_created = Book.objects.get_or_create(
                            title=row.get("title"),
                            author=author,
                            publication_date=row.get("publication_date"),
                            isbn=row.get("isbn")
                        )

                        genre_names = [genre.strip() for genre in row.get("genre_names").split(";")]
                        for genre_name in genre_names:
                            genre, _ = Genre.objects.get_or_create(name=genre_name)
                            book.genres.add(genre)

                        if book_created:
                            created += 1

                    except Exception as e:
                        messages.error(request, f"Ошибка: {e}")

                messages.success(request, f"Импорт завершен. Создано {created} книг")
                return redirect("admin:index")
        else:
            form = CSVImportForm()

        return render(request, "admin/import_csv_form.html", {"form": form})
