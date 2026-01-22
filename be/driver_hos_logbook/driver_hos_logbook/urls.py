from django.contrib import admin
from django.urls import path, include
from django.conf import settings

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
    )
]