from django.urls import path
from . import views

app_name = "professor"

urlpatterns = [
    path("dashboard/", views.dashboard_professor, name="dashboard_professor"),
    # Alunos
    path("alunos/adicionar/", views.adicionar_aluno, name="adicionar_aluno"),
    path("alunos/", views.listar_alunos, name="listar_alunos"),
    path("alunos/editar/<int:aluno_id>/", views.editar_aluno, name="editar_aluno"),
    path("alunos/remover/<int:aluno_id>/", views.remover_aluno, name="remover_aluno"),
    # Avisos
    path("avisos/", views.listar_avisos_professor, name="listar_avisos_professor"),
    path("avisos/adicionar/", views.adicionar_aviso, name="adicionar_aviso"),
    path("avisos/editar/<int:aviso_id>/", views.editar_aviso, name="editar_aviso"),
    path("avisos/remover/<int:aviso_id>/", views.remover_aviso, name="remover_aviso"),
    # Frequência
    path("frequencia/registrar/", views.registrar_frequencia_lote, name="registrar_frequencia"),
    path("frequencia/listar/", views.listar_frequencias, name="listar_frequencias"),
]

