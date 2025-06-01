from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from core.professor.models import Aluno, Frequencia
from core.avisos.models import Aviso
from django.utils import timezone

# Decorator para verificar se o usuário é um aluno
def aluno_required(view_func ):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        is_aluno = False
        try:
            # Verificar se existe um perfil Aluno associado ao usuário logado
            aluno = Aluno.objects.filter(user=request.user).first()
            if aluno:
                is_aluno = True
                # Adicionar o objeto aluno ao request para fácil acesso nas views
                request.aluno = aluno
        except (ObjectDoesNotExist, AttributeError):
            pass

        if not is_aluno:
            return HttpResponseForbidden("Acesso negado. Esta área é restrita a alunos.")

        # Se chegou até aqui, o usuário é um aluno.
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@aluno_required
def dashboard_aluno(request):
    # Obter o objeto aluno associado ao usuário logado
    aluno = request.aluno
    
    # Obter informações relevantes para o dashboard
    frequencias = Frequencia.objects.filter(aluno=aluno).order_by('-data')
    frequencias_recentes = frequencias[:5]  # Últimas 5 frequências
    
    # Calcular estatísticas de presença
    total_frequencias = frequencias.count()
    presencas = frequencias.filter(presente=True).count()
    
    # Calcular taxa de presença (evitar divisão por zero)
    taxa_presenca = (presencas / total_frequencias * 100) if total_frequencias > 0 else 0
    
    context = {
        'aluno': aluno,
        'frequencias_recentes': frequencias_recentes,
        'total_frequencias': total_frequencias,
        'presencas': presencas,
        'taxa_presenca': taxa_presenca,
        'data_atual': timezone.now().date(),
        'page_title': 'Painel do Aluno'
    }
    return render(request, 'aluno/dashboard.html', context)

@aluno_required
def ver_frequencias(request):
    # Obter o objeto aluno associado ao usuário logado
    aluno = request.aluno
    
    # Obter todas as frequências do aluno
    frequencias = Frequencia.objects.filter(aluno=aluno).order_by('-data')
    
    context = {
        'aluno': aluno,
        'frequencias': frequencias,
        'page_title': 'Minhas Frequências'
    }
    return render(request, 'aluno/frequencias.html', context)

@aluno_required
def avisos_aluno(request):
    # Obter o objeto aluno associado ao usuário logado
    aluno = request.aluno
    
    # Obter todos os avisos disponíveis para o aluno
    # Aqui você pode filtrar por turma, curso, etc. dependendo do seu modelo
    avisos = Aviso.objects.filter(
        data_expiracao__gte=timezone.now().date()
    ).order_by('-data_publicacao')
    
    context = {
        'aluno': aluno,
        'avisos': avisos,
        'page_title': 'Avisos'
    }
    return render(request, 'aluno/avisos.html', context)

@aluno_required
def rendimento_aluno(request):
    # Obter o objeto aluno associado ao usuário logado
    aluno = request.aluno
    
    # Aqui você pode adicionar lógica para buscar notas, médias, etc.
    # Por enquanto, estamos apenas passando o objeto aluno para o template
    
    context = {
        'aluno': aluno,
        'page_title': 'Meu Rendimento'
    }
    return render(request, 'aluno/rendimento.html', context)

@aluno_required
def documentacao_aluno(request):
    # Obter o objeto aluno associado ao usuário logado
    aluno = request.aluno
    
    # Aqui você pode adicionar lógica para buscar documentos disponíveis
    # Por enquanto, estamos apenas passando o objeto aluno para o template
    
    context = {
        'aluno': aluno,
        'page_title': 'Documentação'
    }
    return render(request, 'aluno/documentacao.html', context)

@aluno_required
def conteudos_aluno(request):
    # Obter o objeto aluno associado ao usuário logado
    aluno = request.aluno
    
    # Aqui você pode adicionar lógica para buscar conteúdos por disciplina
    # Por enquanto, estamos apenas passando o objeto aluno para o template
    
    context = {
        'aluno': aluno,
        'page_title': 'Conteúdos'
    }
    return render(request, 'aluno/conteudos.html', context)
