# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'frequencia'

urlpatterns = [
    # URLs para Professores
    path('professor/turmas/', views.listar_turmas_professor, name='listar_turmas_professor'),
    path('professor/turma/<int:turma_id>/', views.detalhes_turma_professor, name='detalhes_turma_professor'),
    path('professor/turma/<int:turma_id>/aula/<int:aula_id>/presenca/', views.registrar_presenca, name='registrar_presenca'),
    path('professor/turma/<int:turma_id>/notas/', views.registrar_notas, name='registrar_notas'),
    path('professor/turma/<int:turma_id>/criar_aula/', views.criar_aula, name='criar_aula'),

    # URLs para Alunos
    path('aluno/minhas_turmas/', views.listar_turmas_aluno, name='listar_turmas_aluno'),
    path('aluno/turma/<int:turma_id>/frequencia/', views.ver_frequencia_aluno, name='ver_frequencia_aluno'),
    path('aluno/turma/<int:turma_id>/notas/', views.ver_notas_aluno, name='ver_notas_aluno'),
]

