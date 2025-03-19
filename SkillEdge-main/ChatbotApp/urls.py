from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_page, name='chatbot_page'),
    path('send/', views.chatbot_api, name='chatbot_api'),
]
