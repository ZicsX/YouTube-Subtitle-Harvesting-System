from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('harvester.urls')),
    path("admin/", admin.site.urls),
]
