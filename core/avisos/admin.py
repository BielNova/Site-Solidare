# avisos/admin.py
from django.contrib import admin
from .models import Aviso

@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'data_publicacao', 'data_expiracao', 'autor')
    search_fields = ('titulo', 'conteudo')
    list_filter = ('categoria', 'data_publicacao')
