# recommendation/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('recommendation/', views.recommendation_dashboard, name='recommendation_dashboard'),
]
