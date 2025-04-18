# avisos/admin.py
from django.contrib import admin
from .models import Aviso
from .models import Cliente, Transacao

admin.site.register(Cliente)
admin.site.register(Transacao)


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'data_publicacao', 'data_expiracao', 'autor')
    search_fields = ('titulo', 'conteudo')
    list_filter = ('categoria', 'data_publicacao')
