from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Aluno(models.Model):
    nome_completo = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50, unique=True)
    cadastrado_por = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='alunos_cadastrados')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    curso = models.CharField(max_length=100)
    # Este é o campo que você adicionou e que precisa de migração
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='aluno_profile')

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula}) ({self.curso})"

class Frequencia(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='frequencias')
    data = models.DateField(default=timezone.now)
    presente = models.BooleanField(default=False)
    registrado_por = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='frequencias_registradas')
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('aluno', 'data') # Garante que só há um registro de frequência por aluno por dia
        ordering = ['-data', 'aluno__nome_completo']

    def __str__(self):
        return f"Frequência de {self.aluno.nome_completo} em {self.data.strftime('%d/%m/%Y')} - {'Presente' if self.presente else 'Ausente'}"

# Exemplo de modelo para Turma, se necessário no futuro:
# class Turma(models.Model):
#     nome = models.CharField(max_length=100)
#     professor_responsavel = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)
#     alunos = models.ManyToManyField(Aluno, blank=True)
#
#     def __str__(self):
#         return self.nome