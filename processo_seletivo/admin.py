# processo_seletivo/admin.py
from django.contrib import admin
from .models import Curso, ProcessoSeletivo, Inscricao

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'vagas_total', 'idade_minima', 'idade_maxima')
    search_fields = ('nome', 'descricao')
    list_filter = ('ativo',)

@admin.register(ProcessoSeletivo)
class ProcessoSeletivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_inicio_inscricoes', 'data_fim_inscricoes', 'ativo', 'esta_aberto_para_inscricoes')
    search_fields = ('nome', 'descricao')
    list_filter = ('ativo', 'data_inicio_inscricoes', 'data_fim_inscricoes')
    filter_horizontal = ('cursos_oferecidos',) # Para gerenciar ManyToMany de forma mais amigável

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = (
        'nome_completo_crianca',
        'curso_escolhido',
        'processo_seletivo',
        'status',
        'nome_responsavel',
        'email_responsavel',
        'data_inscricao'
    )
    list_filter = ('status', 'processo_seletivo', 'curso_escolhido')
    search_fields = (
        'nome_completo_crianca',
        'nome_responsavel',
        'cpf_responsavel',
        'email_responsavel',
        'cpf_crianca'
    )
    raw_id_fields = ('processo_seletivo', 'curso_escolhido') # Pode ser útil para muitos registros