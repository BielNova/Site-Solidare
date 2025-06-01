from django.urls import path
from . import views

app_name = 'aluno'

urlpatterns = [
    path('dashboard/', views.dashboard_aluno, name='dashboard_aluno'),
    path('frequencias/', views.ver_frequencias, name='ver_frequencias'),
    path('avisos/', views.avisos_aluno, name='avisos_aluno'),
    path('rendimento/', views.rendimento_aluno, name='rendimento_aluno'),
    path('documentacao/', views.documentacao_aluno, name='documentacao_aluno'),
    path('conteudos/', views.conteudos_aluno, name='conteudos_aluno'),
]
