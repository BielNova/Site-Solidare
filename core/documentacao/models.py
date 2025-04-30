# -*- coding: utf-8 -*-
from django.db import models
from core.user.models import UserProfile
from core.frequencia.models import Curso, Turma # Importar modelos relevantes
import uuid

class Certificado(models.Model):
    # Corrigido: ForeignKey para UserProfile
    aluno = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="certificados") # Corrigido: Removido \
    # Corrigido: ForeignKey para Turma (ou Curso, dependendo da necessidade - Turma parece mais específico)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="certificados") # Corrigido: Removido \
    # Data em que o certificado foi gerado/emitido
    data_emissao = models.DateTimeField(auto_now_add=True)
    # Código único para validação/identificação do certificado
    codigo_validacao = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # O arquivo PDF será gerado dinamicamente, não armazenado diretamente no modelo.
    # Removido: arquivo = models.FileField(upload_to=\'certificados/\')

    def __str__(self):
        # Corrigido: Removido \
        return f"Certificado de {self.aluno.user.username} para {self.turma.curso.nome} - {self.turma.nome}"

    class Meta:
        # Garante que um aluno só tenha um certificado por turma (ajustar se necessário)
        # Corrigido: Removido \
        unique_together = ("aluno", "turma")
        ordering = ["-data_emissao"]

