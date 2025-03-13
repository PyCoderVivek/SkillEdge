"""
URL configuration for SkillEdge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Authentication.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomePage , name='Home'),
    path('skilledge/' , DashBoard , name="Dashboard"),
    path('auth/', include('Authentication.urls')),
    path('performance/', include('Performance.urls')),
    path('recommendation/', include('Recommendation.urls')), 
    path('chatbot/', include('ChatbotApp.urls')),
    path('roadmap/', include('CareerRoadmap.urls')),
    path('community/', include('Community.urls')),
]

