# core/user/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URL para a view de login
    # Use name=\'login\' na tag {% url %} no template
    path(\'login/\', views.login_view, name=\'login\'), 
    
    # --- NOVA URL PARA A VIEW DE REGISTRO --- 
    # Use name=\'register\' na tag {% url %} no template
    path(\'register/\', views.register_view, name=\'register\'),
    
    # URL para a view de logout (exemplo)
    path(\'logout/\', views.logout_view, name=\'logout\'),
    
    # Adicione outras URLs do app user aqui, se necessário
]
