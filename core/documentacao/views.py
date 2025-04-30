# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from weasyprint import HTML, CSS
from .models import Certificado
from core.user.models import UserProfile
# Importar a função de verificação de aluno (se movida para um local comum, senão copiar/adaptar)
from core.frequencia.views import is_aluno # Reutilizando a função de verificação
import os
from django.conf import settings # Para acessar caminhos de arquivos estáticos se necessário

@login_required
@user_passes_test(is_aluno)
def listar_certificados_aluno(request):
    """Lista os certificados disponíveis para o aluno logado."""
    aluno_profile = get_object_or_404(UserProfile, user=request.user)
    # Corrigido: Removido \
    certificados = Certificado.objects.filter(aluno=aluno_profile).select_related("turma__curso")
    return render(request, "documentacao/listar_certificados.html", {"certificados": certificados})

@login_required
@user_passes_test(is_aluno)
def gerar_certificado_pdf(request, codigo_validacao):
    """Gera e retorna o PDF de um certificado específico."""
    aluno_profile = get_object_or_404(UserProfile, user=request.user)
    # Garante que o aluno só possa baixar seu próprio certificado
    certificado = get_object_or_404(Certificado, codigo_validacao=codigo_validacao, aluno=aluno_profile)

    # Contexto para o template do certificado
    context = {
        "aluno_nome": certificado.aluno.user.get_full_name() or certificado.aluno.user.username,
        "curso_nome": certificado.turma.curso.nome,
        "turma_nome": certificado.turma.nome,
        "data_emissao": certificado.data_emissao,
        "codigo_validacao": certificado.codigo_validacao,
        # Adicionar mais informações se necessário (ex: carga horária, nome do professor)
        # "carga_horaria": certificado.turma.curso.carga_horaria, # Exemplo, se existir no modelo Curso
        # "professor_nome": certificado.turma.curso.professor.get_full_name(), # Exemplo
    }

    # Renderiza o template HTML do certificado
    html_string = render_to_string("documentacao/certificado_template.html", context)

    # Define o nome do arquivo PDF
    # Corrigido: Removido \
    filename = f"certificado_{certificado.aluno.user.username}_{certificado.turma.curso.nome}.pdf".replace(" ", "_")

    # Cria o objeto HttpResponse com o tipo de conteúdo PDF
    response = HttpResponse(content_type="application/pdf")
    # Corrigido: Removido \
    response["Content-Disposition"] = f"inline; filename={filename}" # inline para abrir no navegador, attachment para baixar direto

    # Define o CSS (pode ser um arquivo externo ou string)
    # Exemplo usando um arquivo CSS estático (requer configuração de arquivos estáticos no settings.py)
    # css_path = os.path.join(settings.STATIC_ROOT, "css/certificado_style.css")
    # css = CSS(filename=css_path)
    # Exemplo com CSS inline básico:
    css_string = """
        @page {
            size: A4 landscape;
            margin: 1cm;
        }
        body {
            font-family: "Noto Sans CJK SC", "WenQuanYi Zen Hei", sans-serif; /* Usando fontes recomendadas */
            text-align: center;
        }
        h1 {
            color: #444;
        }
        .codigo {
            font-size: 0.8em;
            color: #666;
            margin-top: 30px;
        }
        /* Adicionar mais estilos conforme necessário */
    """
    css = CSS(string=css_string)

    # Gera o PDF usando WeasyPrint
    HTML(string=html_string).write_pdf(response, stylesheets=[css])

    return response

# TODO: Adicionar view para validação pública de certificado (opcional)
# def validar_certificado(request, codigo_validacao):
#    certificado = get_object_or_404(Certificado, codigo_validacao=codigo_validacao)
#    # Renderizar uma página mostrando os detalhes do certificado para validação
#    return render(request, "documentacao/validar_certificado.html", {"certificado": certificado})

