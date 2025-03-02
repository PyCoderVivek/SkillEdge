from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',views.Login , name="Login"),
    path('signup/',views.Signup , name="Signup"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)