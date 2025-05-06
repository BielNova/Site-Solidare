from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Professor, Aluno, Frequencia
from .forms import AlunoForm, AvisoForm, FrequenciaLoteForm
from core.avisos.models import Aviso
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

# Decorator para verificar se o usuário é um professor
def professor_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        is_professor_profile_linked = False
        try:
            if request.user.professor and isinstance(request.user.professor, Professor):
                is_professor_profile_linked = True
        except ObjectDoesNotExist:
            # O perfil Professor não existe para este usuário.
            pass # is_professor_profile_linked permanece False

        if not is_professor_profile_linked:
            # Se o usuário for superuser ou staff e não tiver um perfil de professor, tenta criar um.
            if request.user.is_superuser or request.user.is_staff:
                # Professor.objects.get_or_create(user=request.user) não atribui automaticamente a request.user.professor
                # É preciso re-consultar ou confiar que a relação foi estabelecida.
                profile, created = Professor.objects.get_or_create(user=request.user)
                if profile:
                    # Tenta verificar novamente se o perfil está acessível através do usuário.
                    # É importante que o Django consiga resolver request.user.professor após a criação.
                    # Para garantir, podemos re-verificar:
                    try:
                        if request.user.professor and isinstance(request.user.professor, Professor):
                            is_professor_profile_linked = True
                        else:
                            # Mesmo após get_or_create, a relação não está como esperado.
                            return HttpResponseForbidden("Acesso negado. Falha ao verificar perfil de professor para admin/staff após criação.")
                    except ObjectDoesNotExist:
                        return HttpResponseForbidden("Acesso negado. Perfil de professor não encontrado para admin/staff após tentativa de criação.")
                else:
                    # Isso não deveria acontecer se o usuário existe e get_or_create foi chamado.
                    return HttpResponseForbidden("Acesso negado. Falha crítica ao tentar criar perfil de professor para admin/staff.")
            
            # Se ainda não for um professor (não admin/staff ou falha na criação para admin/staff)
            if not is_professor_profile_linked:
                 return HttpResponseForbidden("Acesso negado. Esta área é restrita a professores.")
        
        # Se chegou até aqui, o usuário é um professor.
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@professor_required
def dashboard_professor(request):
    alunos_count = Aluno.objects.filter(cadastrado_por=request.user.professor).count()
    avisos_count = Aviso.objects.filter(autor=request.user).count()
    frequencias_hoje_count = Frequencia.objects.filter(registrado_por=request.user.professor, data=timezone.now().date()).count()
    context = {
        'alunos_count': alunos_count,
        'avisos_count': avisos_count,
        'frequencias_hoje_count': frequencias_hoje_count,
        'page_title': 'Painel do Professor'
    }
    return render(request, 'professor/dashboard.html', context)

# --- Views de Alunos ---
@professor_required
def adicionar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.cadastrado_por = request.user.professor
            aluno.save()
            messages.success(request, f'Aluno {aluno.nome_completo} adicionado com sucesso!')
            return redirect('professor:listar_alunos')
    else:
        form = AlunoForm()
    context = {
        'form': form,
        'page_title': 'Adicionar Novo Aluno'
    }
    return render(request, 'professor/adicionar_aluno.html', context)

@professor_required
def listar_alunos(request):
    alunos = Aluno.objects.filter(cadastrado_por=request.user.professor).order_by('nome_completo')
    context = {
        'alunos': alunos,
        'page_title': 'Meus Alunos'
    }
    return render(request, 'professor/listar_alunos.html', context)

@professor_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id, cadastrado_por=request.user.professor)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dados do aluno {aluno.nome_completo} atualizados com sucesso!')
            return redirect('professor:listar_alunos')
    else:
        form = AlunoForm(instance=aluno)
    context = {
        'form': form,
        'aluno': aluno,
        'page_title': f'Editar Aluno: {aluno.nome_completo}'
    }
    return render(request, 'professor/editar_aluno.html', context)

@professor_required
def remover_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id, cadastrado_por=request.user.professor)
    if request.method == 'POST':
        nome_aluno = aluno.nome_completo
        aluno.delete()
        messages.success(request, f'Aluno {nome_aluno} removido com sucesso!')
        return redirect('professor:listar_alunos')
    context = {
        'aluno': aluno,
        'page_title': f'Confirmar Remoção: {aluno.nome_completo}'
    }
    return render(request, 'professor/remover_aluno_confirm.html', context)

# --- Views de Avisos ---
@professor_required
def listar_avisos_professor(request):
    avisos = Aviso.objects.filter(autor=request.user).order_by('-data_publicacao')
    context = {
        'avisos': avisos,
        'page_title': 'Meus Avisos'
    }
    return render(request, 'professor/listar_avisos.html', context)

@professor_required
def adicionar_aviso(request):
    if request.method == 'POST':
        form = AvisoForm(request.POST, request.FILES)
        if form.is_valid():
            aviso = form.save(commit=False)
            aviso.autor = request.user
            aviso.save()
            messages.success(request, f'Aviso "{aviso.titulo}" adicionado com sucesso!')
            return redirect('professor:listar_avisos_professor')
    else:
        form = AvisoForm()
    context = {
        'form': form,
        'page_title': 'Adicionar Novo Aviso'
    }
    return render(request, 'professor/adicionar_aviso.html', context)

@professor_required
def editar_aviso(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id, autor=request.user)
    if request.method == 'POST':
        form = AvisoForm(request.POST, request.FILES, instance=aviso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Aviso "{aviso.titulo}" atualizado com sucesso!')
            return redirect('professor:listar_avisos_professor')
    else:
        form = AvisoForm(instance=aviso)
    context = {
        'form': form,
        'aviso': aviso,
        'page_title': f'Editar Aviso: {aviso.titulo}'
    }
    return render(request, 'professor/editar_aviso.html', context)

@professor_required
def remover_aviso(request, aviso_id):
    aviso = get_object_or_404(Aviso, id=aviso_id, autor=request.user)
    if request.method == 'POST':
        titulo_aviso = aviso.titulo
        aviso.delete()
        messages.success(request, f'Aviso "{titulo_aviso}" removido com sucesso!')
        return redirect('professor:listar_avisos_professor')
    context = {
        'aviso': aviso,
        'page_title': f'Confirmar Remoção do Aviso: {aviso.titulo}'
    }
    return render(request, 'professor/remover_aviso_confirm.html', context)

# --- Views de Frequência ---
@professor_required
def registrar_frequencia_lote(request):
    professor = request.user.professor
    # Passa a lista de alunos para o formulário poder renderizar os campos corretamente no template
    alunos_do_professor_list = Aluno.objects.filter(cadastrado_por=professor).order_by("nome_completo")

    if request.method == 'POST':
        form = FrequenciaLoteForm(request.POST, professor=professor)
        if form.is_valid():
            data_frequencia = form.cleaned_data['data']
            try:
                with transaction.atomic():
                    for aluno in alunos_do_professor_list:
                        presente = form.cleaned_data.get(f'aluno_{aluno.id}_presente', False)
                        observacao = form.cleaned_data.get(f'aluno_{aluno.id}_observacao', '')
                        
                        Frequencia.objects.update_or_create(
                            aluno=aluno,
                            data=data_frequencia,
                            defaults={
                                'presente': presente,
                                'observacao': observacao,
                                'registrado_por': professor
                            }
                        )
                messages.success(request, f'Frequência para o dia {data_frequencia.strftime("%d/%m/%Y")} registrada/atualizada com sucesso!')
                return redirect('professor:listar_frequencias')
            except Exception as e:
                messages.error(request, f"Erro ao registrar frequência: {e}")
    else:
        form = FrequenciaLoteForm(professor=professor, initial={'data': timezone.now().date()})
    
    # Adiciona a lista de alunos ao contexto para o template iterar corretamente
    form.alunos_do_professor_list = alunos_do_professor_list 
    context = {
        'form': form,
        'page_title': 'Registrar Frequência em Lote'
    }
    return render(request, 'professor/registrar_frequencia_lote.html', context)

@professor_required
def listar_frequencias(request):
    frequencias = Frequencia.objects.filter(registrado_por=request.user.professor).select_related('aluno').order_by('-data', 'aluno__nome_completo')
    context = {
        'frequencias': frequencias,
        'page_title': 'Histórico de Frequências'
    }
    return render(request, 'professor/listar_frequencias.html', context)

