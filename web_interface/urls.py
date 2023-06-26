from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api-key/', views.api_key, name='api_key'),
    path('queries/', views.queries, name='queries'),
]
