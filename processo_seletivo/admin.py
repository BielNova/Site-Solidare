# processo_seletivo/admin.py

from django.contrib import admin
from .models import Inscricao # Importamos SOMENTE Inscricao

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = (
        'nome_completo',
        'cpf',
        'data_nascimento',
        'email',
        'telefone',
        'sexo',
        'cor',
        'nivel_escolaridade',
        'trabalha',
        'plano_saude',
        'acompanhamento_medico',
        'deficiencia_fisica',
        'deficiencia_mental',
        'tipo_moradia',
        'renda_familiar_total',
    )
    list_filter = (
        'sexo',
        'cor',
        'nivel_escolaridade',
        'rede_ensino',
        'trabalha',
        'apadrinhado',
        'bolsista',
        'familia_participa',
        'conhece_eca',
        'conselho_direito',
        'forum_social',
        'nocao_direitos',
        'referencia_familiar',
        'plano_saude',
        'acompanhamento_medico',
        'cirurgia',
        'deficiencia_fisica',
        'deficiencia_mental',
        'participa_grupos',
        'tipo_moradia',
        'material_construcao',
        'tem_banheiro',
        'energia_eletrica',
        'cadastro_unico',
        'bolsa_familia',
        'beneficio_bpc',
        'renda_familiar_total',
    )
    search_fields = (
        'nome_completo',
        'cpf',
        'email',
        'telefone',
        'bairro_residencia',
        'qual_plano_saude',
        'qual_problema_saude',
        'qual_cirurgia',
        'qual_deficiencia_fisica',
        'qual_grupo_comunitario',
    )