# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from fpdf2 import FPDF # Corrigido: Importar fpdf2
from .models import Certificado
from core.user.models import UserProfile
from core.frequencia.views import is_aluno # Reutilizando a função de verificação

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
    pdf = FPDF(orientation="L", unit="mm", format="A4") # Paisagem A4
    pdf.add_page()

    # Adicionar fonte que suporte caracteres PT-BR
    font_name = "Helvetica" # Default fallback font
    try:
        # Usando fonte NotoSansCJK pré-instalada para suporte a PT-BR/UTF-8
        pdf.add_font("NotoSansCJK", fname="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
        font_name = "NotoSansCJK" # Use NotoSansCJK if loaded successfully
        print("Fonte NotoSansCJK carregada com sucesso.") # Add print for debugging
    except RuntimeError as e:
        print(f"Erro ao carregar fonte TTF NotoSansCJK: {e}")
        print("Usando fonte Helvetica como fallback.") # Add print for debugging

    pdf.set_font(font_name, size=12) # Set the initial font

    # Título
    pdf.set_font(font_name, "B", 20) # Usar font_name
    pdf.cell(0, 20, "CERTIFICADO DE CONCLUSÃO", ln=1, align="C")
    pdf.ln(15) # Quebra de linha maior

    # Corpo do Texto
    pdf.set_font(font_name, "", 12) # Usar font_name

    # Usar multi_cell para texto mais longo e centralizado
    pdf.set_x(30) # Recuo esquerdo
    pdf.set_font(font_name, "", 14) # Usar font_name
    pdf.multi_cell(237, 10, f"Certificamos que", align="C")
    pdf.set_font(font_name, "B", 16) # Usar font_name
    # Garantir que o nome seja string antes de passar para multi_cell
    aluno_nome_completo = certificado.aluno.user.get_full_name() or certificado.aluno.user.username
    pdf.multi_cell(237, 10, f"{str(aluno_nome_completo)}", align="C") # Convertido para str
    pdf.set_font(font_name, "", 14) # Usar font_name
    pdf.multi_cell(237, 10, f"concluiu com sucesso o curso de", align="C")
    pdf.set_font(font_name, "B", 16) # Usar font_name
    pdf.multi_cell(237, 10, f"{str(certificado.turma.curso.nome)}", align="C") # Convertido para str
    pdf.set_font(font_name, "", 14) # Usar font_name
    pdf.multi_cell(237, 10, f"(Turma: {str(certificado.turma.nome)}), oferecido pelo Instituto Solidare.", align="C") # Convertido para str

    pdf.ln(20)

    # Data e Código
    pdf.set_font(font_name, "", 10) # Usar font_name
    pdf.cell(0, 10, f"Emitido em: {certificado.data_emissao.strftime('%d/%m/%Y')}", ln=1, align="C")
    pdf.cell(0, 10, f"Código de Validação: {str(certificado.codigo_validacao)}", ln=1, align="C") # Convertido para str

    # --- Fim Lógica FPDF2 ---

    # Define o nome do arquivo PDF
    filename = f"certificado_{certificado.aluno.user.username}_{certificado.turma.curso.nome}.pdf".replace(" ", "_")

    # Gera a saída do PDF como bytes
    pdf_output = pdf.output(dest="S") # Corrigido: Retorna bytes diretamente

    # Cria o objeto HttpResponse com o tipo de conteúdo PDF, passando os bytes
    response = HttpResponse(pdf_output, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename={filename}" # inline para abrir no navegador

    return response

# View de validação (mantida como TODO)
# def validar_certificado(request, codigo_validacao):
#    certificado = get_object_or_404(Certificado, codigo_validacao=codigo_validacao)
#    return render(request, "documentacao/validar_certificado.html", {"certificado": certificado})

