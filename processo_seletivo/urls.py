# processo_seletivo/urls.py
from django.urls import path
from . import views

app_name = 'processo_seletivo' # Define um namespace para as URLs do app

urlpatterns = [
    path('inscricoes/', views.lista_processos_seletivos, name='lista_processos_seletivos'),
    # Vamos adicionar mais URLs aqui conforme avançamos
]