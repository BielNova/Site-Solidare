from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Aviso(models.Model):
    CATEGORIAS = [
        ('geral', 'Geral'),
        ('fundamental', 'Ensino Fundamental'),
        ('medio', 'Ensino Médio'),
        ('tecnico', 'Curso Técnico'),
    ]

    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='geral')
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField(null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    anexo = models.FileField(upload_to='avisos/anexos/', null=True, blank=True)

    def __str__(self):
        return self.titulo

    def is_expired(self):
        
        if self.data_expiracao and self.data_expiracao < timezone.now():
            return True
        return False
