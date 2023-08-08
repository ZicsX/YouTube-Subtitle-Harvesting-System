from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("start/", views.start_process, name="start"),
    path("stop/", views.stop_process, name="stop"),
    path("status/", views.system_status, name="status"),
    path("update_api_key/", views.update_api_key, name="update_api_key"),
]
