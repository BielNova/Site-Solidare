# Full views.py content
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
from django.contrib.auth.models import User # Import User model
from django import forms  # Adicionado para o HiddenInput

# Decorator para verificar se o usuário é um professor
def professor_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        is_professor_profile_linked = False
        try:
            # Verifica se existe um perfil Professor associado ao usuário logado
            if hasattr(request.user, 'professor') and isinstance(request.user.professor, Professor):
                is_professor_profile_linked = True
        except ObjectDoesNotExist:
            # O perfil Professor não existe para este usuário.
            pass # is_professor_profile_linked permanece False

        # Se não for professor E for superuser/staff, tenta criar o perfil
        if not is_professor_profile_linked and (request.user.is_superuser or request.user.is_staff):
            profile, created = Professor.objects.get_or_create(user=request.user)
            if profile:
                # Força o recarregamento do usuário para garantir que a relação reversa funcione
                request.user.refresh_from_db()
                try:
                    if hasattr(request.user, 'professor') and isinstance(request.user.professor, Professor):
                        is_professor_profile_linked = True
                    else:
                        # Mesmo após get_or_create, a relação não está como esperado.
                        return HttpResponseForbidden("Acesso negado. Falha ao verificar perfil de professor para admin/staff após criação.")
                except ObjectDoesNotExist:
                     return HttpResponseForbidden("Acesso negado. Perfil de professor não encontrado para admin/staff após tentativa de criação.")
            else:
                # Falha crítica
                return HttpResponseForbidden("Acesso negado. Falha crítica ao tentar criar perfil de professor para admin/staff.")

        # Se ainda não for um professor (nem admin/staff que teve perfil criado)
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
    # Buscar IDs de usuários que já são professores
    professor_user_ids = Professor.objects.values_list('user_id', flat=True)
    
    # Buscar IDs de usuários que já são alunos
    aluno_user_ids = Aluno.objects.exclude(user=None).values_list('user_id', flat=True)
    
    # Buscar usuários que NÃO são professores, NÃO são alunos e NÃO são superusuários
    eligible_users = User.objects.exclude(
        id__in=list(professor_user_ids) + list(aluno_user_ids)
    ).exclude(is_superuser=True).order_by('username')

    if request.method == 'POST':
        # Passar o queryset de usuários elegíveis para o formulário para validação
        form = AlunoForm(request.POST, eligible_users=eligible_users)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.cadastrado_por = request.user.professor
            
            selected_user = form.cleaned_data.get('usuario_existente')
            # Se um usuário existente foi selecionado, associá-lo ao aluno
            if selected_user:
                aluno.user = selected_user
                # Se o nome completo não foi preenchido, usar o nome do usuário selecionado
                if not form.cleaned_data.get('nome_completo'):
                    aluno.nome_completo = selected_user.get_full_name() or selected_user.username
            # Se nome_completo foi preenchido, ele tem precedência
            elif form.cleaned_data.get('nome_completo'):
                 aluno.nome_completo = form.cleaned_data.get('nome_completo')

            # Verificar se a matrícula já existe
            if Aluno.objects.filter(matricula=aluno.matricula).exists():
                messages.error(request, f'A matrícula "{aluno.matricula}" já está em uso.')
            else:
                aluno.save()
                messages.success(request, f'Aluno {aluno.nome_completo} adicionado com sucesso!')
                return redirect('professor:listar_alunos')
        else:
             messages.error(request, "Erro ao adicionar aluno. Verifique os dados informados.")

    else: # GET request
        # Passar o queryset de usuários elegíveis para o formulário para popular o dropdown
        form = AlunoForm(eligible_users=eligible_users)
        
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
    # Não precisamos passar eligible_users aqui, pois não estamos selecionando usuário na edição
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        # Remover o campo usuario_existente dos dados do POST antes de validar, pois ele não pertence ao modelo Aluno
        # Ou melhor, ajustar o form para não incluir esse campo na edição, ou ignorá-lo aqui.
        # Vamos ignorar por enquanto, mas o ideal seria um form diferente para edição.
        if 'usuario_existente' in form.fields:
             form.fields['usuario_existente'].required = False # Make it not required for edit
             form.fields['usuario_existente'].widget = forms.HiddenInput() # Hide it

        if form.is_valid():
            # Verificar se a matrícula foi alterada e se a nova já existe para outro aluno
            nova_matricula = form.cleaned_data.get('matricula')
            if Aluno.objects.filter(matricula=nova_matricula).exclude(id=aluno_id).exists():
                messages.error(request, f'A matrícula "{nova_matricula}" já está em uso por outro aluno.')
            else:
                form.save()
                messages.success(request, f'Dados do aluno {aluno.nome_completo} atualizados com sucesso!')
                return redirect('professor:listar_alunos')
        else:
            messages.error(request, "Erro ao editar aluno. Verifique os dados informados.")
    else:
        form = AlunoForm(instance=aluno)
        if 'usuario_existente' in form.fields:
             form.fields['usuario_existente'].required = False
             form.fields['usuario_existente'].widget = forms.HiddenInput()

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
            messages.error(request, "Erro ao registrar frequência. Verifique os dados informados.")

    else:
        form = FrequenciaLoteForm(professor=professor, initial={'data': timezone.now().date()})
    
    # Adiciona a lista de alunos ao contexto para o template iterar corretamente
    # Esta linha parece redundante pois o form já é inicializado com o professor
    # form.alunos_do_professor_list = alunos_do_professor_list 
    context = {
        'form': form,
        'page_title': 'Registrar Frequência'
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

# --- Views de Avisos ---
@professor_required
def listar_avisos_professor(request):
    # Processar o formulário do modal se for um POST
    if request.method == 'POST':
        form_aviso = AvisoForm(request.POST, request.FILES)
        if form_aviso.is_valid():
            aviso = form_aviso.save(commit=False)
            aviso.autor = request.user
            aviso.save()
            messages.success(request, f'Aviso "{aviso.titulo}" adicionado com sucesso!')
            return redirect('professor:listar_avisos_professor')
        else:
            # Se o formulário for inválido, a página será recarregada abaixo
            # A flag de erro no form fará o modal reabrir via JS no template
            messages.error(request, "Erro ao adicionar aviso. Verifique os dados informados no formulário.")
            # Mantém o form inválido para exibir os erros no modal
    else:
        # Para GET, apenas cria um formulário vazio para o modal
        form_aviso = AvisoForm()

    # Buscar os avisos existentes para exibir na lista
    avisos = Aviso.objects.filter(autor=request.user).order_by('-data_publicacao')
    
    context = {
        'avisos': avisos,
        'form_aviso': form_aviso, # Passa o formulário (novo ou inválido) para o template
        'page_title': 'Meus Avisos'
    }
    return render(request, 'professor/listar_avisos.html', context)


