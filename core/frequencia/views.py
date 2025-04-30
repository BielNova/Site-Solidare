# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import Turma, Aula, Presenca, Nota, UserProfile
from .forms import AulaForm # Removido PresencaFormSet, NotaFormSet
from django.forms import modelformset_factory
import datetime

# Funções de verificação de grupo (simples, pode ser melhorado com permissões do Django)
def is_professor(user):
    # Adapte esta lógica conforme a estrutura de grupos/perfis do seu projeto
    # Exemplo: return user.groups.filter(name=\"Professores\").exists()
    # Por enquanto, vamos assumir que qualquer usuário logado pode ser professor para teste
    # O ideal é ter um campo no UserProfile ou um grupo específico
    return user.is_authenticated # Simplificação temporária

def is_aluno(user):
    # Adapte esta lógica
    # Exemplo: return user.groups.filter(name=\"Alunos\").exists()
    try:
        # Verifica se o usuário tem um perfil e NÃO é professor (simplificação)
        # A lógica de is_professor precisa ser robusta
        return hasattr(user, 'userprofile') # Assumindo que só alunos têm UserProfile por enquanto
    except UserProfile.DoesNotExist:
        return False

# --- Views para Professores ---

@login_required
#@user_passes_test(is_professor) # Descomentar quando a lógica de professor for robusta
def listar_turmas_professor(request):
    # Ajustar para filtrar turmas do professor logado
    # A relação atual está Curso -> Professor. Se um professor pode dar várias turmas do mesmo curso, ok.
    # Se a relação for Turma -> Professor, ajustar o filtro.
    turmas = Turma.objects.filter(curso__professor=request.user)
    return render(request, 'frequencia/professor_turmas_list.html', {"turmas": turmas})

@login_required
#@user_passes_test(is_professor)
def detalhes_turma_professor(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id, curso__professor=request.user)
    aulas = Aula.objects.filter(turma=turma).order_by('data') # Corrigido: removido \ antes de 'data'
    alunos = turma.alunos.all()
    return render(request, 'frequencia/professor_turma_detail.html', {"turma": turma, "aulas": aulas, "alunos": alunos})

@login_required
#@user_passes_test(is_professor)
def criar_aula(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id, curso__professor=request.user)
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            aula = form.save(commit=False)
            aula.turma = turma
            aula.save()
            # Criar registros de presença vazios para a nova aula
            for aluno_profile in turma.alunos.all():
                Presenca.objects.get_or_create(aula=aula, aluno=aluno_profile, defaults={'status': 'F'}) # Default Falta
            return redirect('frequencia:detalhes_turma_professor', turma_id=turma.id)
    else:
        form = AulaForm(initial={'data': datetime.date.today()})
    return render(request, 'frequencia/criar_aula.html', {'form': form, 'turma': turma})

@login_required
#@user_passes_test(is_professor)
def registrar_presenca(request, turma_id, aula_id):
    turma = get_object_or_404(Turma, pk=turma_id, curso__professor=request.user)
    aula = get_object_or_404(Aula, pk=aula_id, turma=turma)
    alunos_da_turma = turma.alunos.all()

    # Garante que todos os alunos da turma tenham um registro de presença para esta aula
    for aluno_profile in alunos_da_turma:
        Presenca.objects.get_or_create(aula=aula, aluno=aluno_profile, defaults={'status': 'F'}) # Default Falta

    # Filtra para pegar apenas as presenças desta aula
    queryset = Presenca.objects.filter(aula=aula).select_related('aluno__user').order_by('aluno__user__first_name', 'aluno__user__last_name') # Corrigido

    # Usar o nome correto do FormSet definido em forms.py ou localmente
    DynamicPresencaFormSet = modelformset_factory(Presenca, fields=('status',), extra=0)

    if request.method == 'POST':
        formset = DynamicPresencaFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect('frequencia:detalhes_turma_professor', turma_id=turma.id)
        else:
            # Adicionar tratamento de erro se necessário
            print(formset.errors)
    else:
        formset = DynamicPresencaFormSet(queryset=queryset)

    # Adiciona nome do aluno ao formset para exibição no template
    for form in formset:
        form.instance.aluno_nome = form.instance.aluno.user.get_full_name() or form.instance.aluno.user.username

    return render(request, 'frequencia/registrar_presenca.html', {
        'formset': formset,
        'aula': aula,
        'turma': turma
    })

@login_required
#@user_passes_test(is_professor)
def registrar_notas(request, turma_id):
    turma = get_object_or_404(Turma, pk=turma_id, curso__professor=request.user)
    alunos = turma.alunos.all().select_related('user')

    # Usaremos um formset para notas, mas a estrutura pode ser complexa.
    # Uma abordagem mais simples pode ser um formulário por aluno/atividade.
    # Vamos tentar um formset para adicionar/editar notas para todos os alunos de uma vez.
    # Isso requer um formulário mais customizado ou lógica na view.

    # Simplificação: Por enquanto, apenas exibe os alunos. A lógica de salvar notas precisa ser implementada.
    # A criação de um NotaFormSet adequado é mais complexa.
    # TODO: Implementar NotaFormSet e lógica de salvamento.

    notas_existentes = Nota.objects.filter(turma=turma).order_by('aluno__user__first_name', 'atividade') # Corrigido

    if request.method == 'POST':
        # Lógica para salvar/atualizar notas viria aqui
        # Exemplo: Iterar sobre request.POST, identificar aluno, atividade, nota e salvar.
        pass # Placeholder

    return render(request, 'frequencia/registrar_notas.html', {
        'turma': turma,
        'alunos': alunos,
        'notas_existentes': notas_existentes
        # 'formset': formset # Passar o formset quando implementado
    })

# --- Views para Alunos ---

@login_required
@user_passes_test(is_aluno)
def listar_turmas_aluno(request):
    aluno_profile = get_object_or_404(UserProfile, user=request.user)
    turmas = aluno_profile.turmas_matriculadas.all().select_related('curso') # Corrigido
    return render(request, 'frequencia/aluno_turmas_list.html', {"turmas": turmas})

@login_required
@user_passes_test(is_aluno)
def ver_frequencia_aluno(request, turma_id):
    aluno_profile = get_object_or_404(UserProfile, user=request.user)
    turma = get_object_or_404(Turma, pk=turma_id, alunos=aluno_profile)
    presencas = Presenca.objects.filter(aluno=aluno_profile, aula__turma=turma).select_related('aula').order_by('aula__data') # Corrigido
    total_aulas = Aula.objects.filter(turma=turma).count()
    total_presente = presencas.filter(status='P').count()
    percentual_presenca = (total_presente / total_aulas * 100) if total_aulas > 0 else 0

    return render(request, 'frequencia/aluno_frequencia.html', {
        'turma': turma,
        'presencas': presencas,
        'total_aulas': total_aulas,
        'total_presente': total_presente,
        'percentual_presenca': round(percentual_presenca, 2)
    })

@login_required
@user_passes_test(is_aluno)
def ver_notas_aluno(request, turma_id):
    aluno_profile = get_object_or_404(UserProfile, user=request.user)
    turma = get_object_or_404(Turma, pk=turma_id, alunos=aluno_profile)
    notas = Nota.objects.filter(aluno=aluno_profile, turma=turma).order_by('data_lancamento') # Corrigido
    return render(request, 'frequencia/aluno_notas.html', {"turma": turma, "notas": notas})

