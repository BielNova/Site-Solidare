from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User

def user(request):
    return render(request, 'user/login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Encontra o usuário pelo email
            user_obj = User.objects.get(email=email)
            # Autentica usando o username encontrado
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                # Usando reverse para garantir que a URL seja resolvida corretamente
                return redirect(reverse('aviso_list'))
            else:
                messages.error(request, 'Senha incorreta.')
        except User.DoesNotExist:
            messages.error(request, 'Email não encontrado.')
            
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
            
            # ADICIONAR ESTA LINHA:
            UserProfile.objects.create(user=user)
            
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
        # resto do código permanece igual

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('login')
