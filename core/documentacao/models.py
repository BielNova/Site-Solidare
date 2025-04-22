from django.db import models

class Certificado(models.Models):
    aluno = models.CharField(max_length=250)
    curso = models.CharField(max_length=250)
    data_emissao = models.DateField()
    arquiv = models.FileField(upload_to='certificados/')

    def __str__(self):
        return f'{self.aluno} - {self.curso}'