# processo_seletivo/views.py

from django.shortcuts import render, redirect
from .models import Inscricao
from .forms import InscricaoForm # Agora o forms.py existe e podemos importá-lo!

def inscrever(request):
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            form.save()
            # Você pode adicionar uma mensagem de sucesso aqui se usar django.contrib.messages
            # from django.contrib import messages
            # messages.success(request, "Sua inscrição foi realizada com sucesso!")
            return redirect('processo_seletivo:inscricao_sucesso') # Redireciona para a URL nomeada
    else:
        form = InscricaoForm()

    context = {
        'form': form,
        'titulo_pagina': 'Formulário de Inscrição'
    }
    return render(request, 'processo_seletivo/inscricao_form.html', context)

def inscricao_sucesso(request):
    return render(request, 'processo_seletivo/inscricao_sucesso.html', {
        'titulo_pagina': 'Inscrição Realizada com Sucesso!'
    })

def lista_inscricoes(request):
    # Opcional: view para listar todas as inscrições. Útil para debug ou admin.
    inscricoes = Inscricao.objects.all().order_by('-id')
    context = {
        'inscricoes': inscricoes,
        'titulo_pagina': 'Lista de Inscrições'
    }
    return render(request, 'processo_seletivo/lista_inscricoes.html', context)