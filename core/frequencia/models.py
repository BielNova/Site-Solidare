# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from core.user.models import UserProfile

# Modelo para Cursos
class Curso(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cursos_lecionados')

    def __str__(self):
        return self.nome

# Modelo para Turmas (grupos de alunos em um curso)
class Turma(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='turmas')
    nome = models.CharField(max_length=100) # Ex: 'Turma A - 2025.1'
    alunos = models.ManyToManyField(UserProfile, related_name='turmas_matriculadas')
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.curso.nome} - {self.nome}'

# Modelo para Aulas
class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='aulas')
    data = models.DateField()
    topico = models.CharField(max_length=255, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['data']

    def __str__(self):
        return f'Aula de {self.turma} em {self.data}'

# Modelo para Registro de Presença
class Presenca(models.Model):
    STATUS_CHOICES = (
        ('P', 'Presente'),
        ('F', 'Falta'),
        ('J', 'Falta Justificada'),
    )
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='presencas')
    aluno = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='presencas')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='F')

    class Meta:
        unique_together = ('aula', 'aluno') # Garante que só haja um registro por aluno por aula

    def __str__(self):
        return f'{self.aluno.user.username} - {self.aula.data} - {self.get_status_display()}'

# Modelo para Notas/Desempenho
class Nota(models.Model):
    aluno = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notas')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='notas')
    atividade = models.CharField(max_length=200) # Ex: 'Prova 1', 'Trabalho Final'
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    data_lancamento = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Nota de {self.aluno.user.username} em {self.atividade} ({self.turma}) - {self.nota}'

