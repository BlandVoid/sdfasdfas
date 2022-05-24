from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Django admin
    path("api/admin/", admin.site.urls),
    # Local
    path("api/result/", include("result.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
