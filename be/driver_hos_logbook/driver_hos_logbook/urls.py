from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urls = [
    {'path': 'logbook/', 'view': include("driver_hos_logbook.apps.driver_hos_logbook.urls")},
]

urlpatterns = [
    path(
        f"{settings.API_PREFIX}{settings.API_VERSION}{item['path']}", 
        item['view']
    ) 
    for item in urls
]

urlpatterns += [
    path(
        "secured-admin/",
        admin.site.urls
    ),

    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    # ReDoc (optional)
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema")),
]