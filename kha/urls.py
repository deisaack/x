from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^a/', admin.site.urls),
    url(r'^academics/', include("academics.urls", namespace='academics')),
    url(r'^administration/', include("administration.urls", namespace='administration')),
    url(r'^library/', include("library.urls", namespace='books')),
    url(r'^portal/', include('portals.urls', namespace='portals')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


