from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from books.sitemaps import BookSitemap, AuthorSitemap, GenreSitemap
from library.admin_views import CSVImportAdminView


sitemaps = {
    "books": BookSitemap,
    "authors": AuthorSitemap,
    "genres": GenreSitemap,
}
urlpatterns = [
    *CSVImportAdminView.get_urls(),
    path('i18n/', include('django.conf.urls.i18n')),
    path("silk/", include("silk.urls", namespace="silk")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(
        r"^favicon\.ico$", RedirectView.as_view(url=settings.STATIC_URL + "favicon.ico")
    ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
)