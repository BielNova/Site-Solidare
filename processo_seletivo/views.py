# processo_seletivo/views.py
from django.shortcuts import render
from django.utils import timezone
from .models import ProcessoSeletivo

def lista_processos_seletivos(request):
    """
    Lista todos os processos seletivos ativos e abertos para inscrição.
    """
    today = timezone.localdate()
    processos_abertos = ProcessoSeletivo.objects.filter(
        ativo=True,
        data_inicio_inscricoes__lte=today, # Início das inscrições é hoje ou antes
        data_fim_inscricoes__gte=today    # Fim das inscrições é hoje ou depois
    ).order_by('-data_inicio_inscricoes') # Ordena do mais recente para o mais antigo

    context = {
        'processos_abertos': processos_abertos,
        'titulo_pagina': 'Processos Seletivos Ativos'
    }
    return render(request, 'processo_seletivo/lista_processos_seletivos.html', context)