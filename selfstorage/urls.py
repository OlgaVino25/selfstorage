from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls")),
    path("", include("main.urls")),
    path("promotions/", include("promotions.urls")),
    path("rent/", include("rent.urls")),
    path("services/", include("services.urls")),
    path("warehouses/", include("warehouses.urls")),
    path("boxes/", include("warehouses.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path(r"__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
