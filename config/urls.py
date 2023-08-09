from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

DESCRIPTION = """simple referal API for HardSystems"""

schema_view = get_schema_view(
    openapi.Info(
        title="HardSystems simple referal API",
        default_version="v1",
        description=DESCRIPTION,
        url="https://simplereferal.com/",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns_api = [
    path("", include("apps.referal.urls_api")),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(urlpatterns_api)),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
