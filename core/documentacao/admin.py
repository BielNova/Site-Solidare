from django.contrib import admin
from .models import Certificado

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    # Corrigido: \"curso\" não é um campo direto. Usando \"turma\" ou um método customizado.
    # Vamos usar \"turma\" e adicionar um método para exibir o nome do curso.
    list_display = ("aluno", "get_curso_nome", "turma", "data_emissao", "codigo_validacao")
    list_filter = ("turma__curso", "data_emissao")
    search_fields = ("aluno__user__username", "turma__nome", "turma__curso__nome", "codigo_validacao")

    # Corrigido: Removido \
    @admin.display(description="Curso")
    def get_curso_nome(self, obj):
        return obj.turma.curso.nome

