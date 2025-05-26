from django.shortcuts import render, redirect
from django.contrib import messages
import random
from .forms import ContatoForm

def home(request):
    return render(request, 'home/index.html')

# View para a página de contato
def contato(request):
    form = ContatoForm()
    
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            assunto = form.cleaned_data['assunto']
            mensagem = form.cleaned_data['mensagem']

            # Imprime as informações no terminal (conforme solicitado para o protótipo)
            print(f'--- Formulário de Contato Recebido ---')
            print(f'Nome: {nome}')
            print(f'Email: {email}')
            print(f'Assunto: {assunto}')
            print(f'Mensagem: {mensagem}')
            print(f'--------------------------------------')

            messages.success(request, 'Sua mensagem foi enviada com sucesso!')
            return redirect('contato') # Redireciona para a mesma página para limpar o formulário

    # Gera um número de telefone aleatório (apenas para exemplo)
    telefone_aleatorio = f'({random.randint(10, 99)}) {random.randint(90000, 99999)}-{random.randint(1000, 9999)}'
    context = {
        'form': form,
        'telefone': telefone_aleatorio
    }
    return render(request, 'home/contato.html', context)
