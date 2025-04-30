# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'documentacao'

urlpatterns = [
    # URL para o aluno listar seus certificados
    path('meus_certificados/', views.listar_certificados_aluno, name='listar_certificados_aluno'),
    # URL para gerar e baixar o PDF de um certificado específico
    path('certificado/<uuid:codigo_validacao>/pdf/', views.gerar_certificado_pdf, name='gerar_certificado_pdf'),
    # Adicionar outras URLs se necessário (ex: validação pública de certificado)
]

