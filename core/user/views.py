from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

def user(request):
    return render(request, 'user/login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Usando reverse para garantir que a URL seja resolvida corretamente
            return redirect(reverse('aviso-list'))
        else:
            messages.error(request, 'Credenciais inválidas.')
    return render(request, 'user/login.html', {'form_type': 'login'})

from django.shortcuts import render, redirect
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
        else:
            # Não adiciona mensagens de erro aqui, pois o template já exibirá os erros do formulário
            # Apenas indica que deve mostrar o formulário de registro
            return render(request, 'user/login.html', {'form': form, 'show_register': True})
    else:
        form = RegisterForm()
    
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('login')
