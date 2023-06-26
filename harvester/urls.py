from django.urls import path

from . import views

urlpatterns = [
    path('api_key/', views.api_key_update, name='api_key'),
    path('seed_query/', views.seed_query_update, name='seed_query'),
    # Add other URLs here as you create more views
]
