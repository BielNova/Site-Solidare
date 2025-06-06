# processo_seletivo/urls.py

from django.urls import path
from . import views

app_name = 'processo_seletivo' # Define o namespace para as URLs do app

urlpatterns = [
    path('inscrever/', views.inscrever, name='inscrever'),
    path('sucesso/', views.inscricao_sucesso, name='inscricao_sucesso'),
    path('lista_inscricoes/', views.lista_inscricoes, name='lista_inscricoes'), # Opcional
    # Lembre-se de remover quaisquer outras URLs que você tinha aqui que
    # apontavam para modelos ou views antigas (Curso, ProcessoSeletivo, etc.)
]