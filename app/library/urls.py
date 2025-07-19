from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from library.admin_views import CSVImportAdminView

urlpatterns = [
    *CSVImportAdminView.get_urls(),
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
]