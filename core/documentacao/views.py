from django.shortcuts import render
from .models import Certificado

def listar_certificados(request):
    certificados = Certificado.objects.all()
    return render(request, 'documentacao/listar_certificados.html', {'certificados': certificados})


