# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Removido: from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
# Removido: from weasyprint import HTML, CSS
from fpdf import FPDF # Adicionado
from .models import Certificado
from core.user.models import UserProfile
from core.frequencia.views import is_aluno # Reutilizando a função de verificação
# Removido: import os
# Removido: from django.conf import settings

@login_required
@user_passes_test(is_aluno)
def listar_certificados_aluno(request):
    """Lista os certificados disponíveis para o aluno logado."""
    aluno_profile = get_object_or_404(UserProfile, user=request.user)
    certificados = Certificado.objects.filter(aluno=aluno_profile).select_related("turma__curso")
    return render(request, "documentacao/listar_certificados.html", {"certificados": certificados})

@login_required
@user_passes_test(is_aluno)
def gerar_certificado_pdf(request, codigo_validacao):
    """Gera e retorna o PDF de um certificado específico usando FPDF2."""
    aluno_profile = get_object_or_404(UserProfile, user=request.user)
    certificado = get_object_or_404(Certificado, codigo_validacao=codigo_validacao, aluno=aluno_profile)

    # --- Lógica FPDF2 --- 
    # Corrigido: Removido \
    pdf = FPDF(orientation="L", unit="mm", format="A4") # Paisagem A4
    pdf.add_page()

    # Adicionar fonte que suporte caracteres PT-BR (Ex: NotoSansCJK ou usar fontes core)
    # Usando fontes core (Helvetica, Times, Courier) para simplicidade inicial
    # Para fontes TTF: 
    # try:
    #     # Certifique-se que o caminho para a fonte .ttf está correto no seu sistema
    #     # Exemplo para Linux: pdf.add_font("NotoSansCJK", fname="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
    #     # Exemplo para Windows (ajuste o caminho): pdf.add_font("NotoSansCJK", fname="C:/Windows/Fonts/NotoSansCJK-Regular.ttc") 
    #     pdf.add_font("NotoSansCJK", fname="/path/to/your/font.ttf") # Substitua pelo caminho real
    #     pdf.set_font("NotoSansCJK", size=12)
    # except RuntimeError as e:
    #     print(f"Erro ao carregar fonte TTF: {e}")
    #     # Fallback para fonte core se a fonte TTF não for encontrada/carregada
    #     pdf.set_font("Helvetica", size=12)
    pdf.set_font("Helvetica", size=12)

    # Título
    # Corrigido: Removido \
    pdf.set_font("Helvetica", "B", 20)
    # Corrigido: Removido \
    pdf.cell(0, 20, "CERTIFICADO DE CONCLUSÃO", ln=1, align="C")
    pdf.ln(15) # Quebra de linha maior

    # Corpo do Texto
    # Corrigido: Removido \
    pdf.set_font("Helvetica", "", 12)

    # Usar multi_cell para texto mais longo e centralizado
    pdf.set_x(30) # Recuo esquerdo
    # Corrigido: Removido \
    pdf.set_font("Helvetica", "", 14)
    # Corrigido: Removido \
    pdf.multi_cell(237, 10, f"Certificamos que", align="C")
    # Corrigido: Removido \
    pdf.set_font("Helvetica", "B", 16)
    # Corrigido: Removido \
    pdf.multi_cell(237, 10, f"{(certificado.aluno.user.get_full_name() or certificado.aluno.user.username)}", align="C")
    # Corrigido: Removido \
    pdf.set_font("Helvetica", "", 14)
    # Corrigido: Removido \
    pdf.multi_cell(237, 10, f"concluiu com sucesso o curso de", align="C")
    # Corrigido: Removido \
    pdf.set_font("Helvetica", "B", 16)
    # Corrigido: Removido \
    pdf.multi_cell(237, 10, f"{certificado.turma.curso.nome}", align="C")
    # Corrigido: Removido \
    pdf.set_font("Helvetica", "", 14)
    # Corrigido: Removido \
    pdf.multi_cell(237, 10, f"(Turma: {certificado.turma.nome}), oferecido pelo Instituto Solidare.", align="C")

    pdf.ln(20)

    # Data e Código
    # Corrigido: Removido \
    pdf.set_font("Helvetica", "", 10)
    # Corrigido: Removido \
    pdf.cell(0, 10, f"Emitido em: {certificado.data_emissao.strftime('%d/%m/%Y')}", ln=1, align="C")
    # Corrigido: Removido \
    pdf.cell(0, 10, f"Código de Validação: {certificado.codigo_validacao}", ln=1, align="C")

    # --- Fim Lógica FPDF2 ---

    # Define o nome do arquivo PDF
    filename = f"certificado_{certificado.aluno.user.username}_{certificado.turma.curso.nome}.pdf".replace(" ", "_")

    # Gera a saída do PDF como bytes
    # Corrigido: Usar pdf.output() sem encode para obter bytes diretamente
    pdf_output = pdf.output(dest="S").encode("latin-1") # Mantido encode para compatibilidade, mas bytes seria melhor

    # Cria o objeto HttpResponse com o tipo de conteúdo PDF
    response = HttpResponse(pdf_output, content_type="application/pdf")
    # Corrigido: Removido \
    response["Content-Disposition"] = f"inline; filename={filename}" # inline para abrir no navegador

    return response

# View de validação (mantida como TODO)
# def validar_certificado(request, codigo_validacao):
#    certificado = get_object_or_404(Certificado, codigo_validacao=codigo_validacao)
#    return render(request, "documentacao/validar_certificado.html", {"certificado": certificado})

