# core/user/urls.py

from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.user, name='user'), 
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),    # Adicione outras URLs do app user aqui, se necessário
]
