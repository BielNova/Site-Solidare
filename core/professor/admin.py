from django.contrib import admin
from .models import Professor, Aluno, Frequencia

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_username', 'get_email')
    search_fields = ('user__username', 'user__email')

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user__username'
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'matricula', 'cadastrado_por', 'data_cadastro')
    search_fields = ('nome_completo', 'matricula')
    list_filter = ('cadastrado_por', 'data_cadastro')
    raw_id_fields = ('cadastrado_por',)

class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'data', 'presente', 'registrado_por_username')
    search_fields = ('aluno__nome_completo', 'aluno__matricula', 'registrado_por__user__username')
    list_filter = ('data', 'presente', 'registrado_por')
    date_hierarchy = 'data'
    raw_id_fields = ('aluno', 'registrado_por')

    def registrado_por_username(self, obj):
        if obj.registrado_por:
            return obj.registrado_por.user.username
        return None
    registrado_por_username.admin_order_field = 'registrado_por__user__username'
    registrado_por_username.short_description = 'Registrado por'

admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Frequencia, FrequenciaAdmin)

