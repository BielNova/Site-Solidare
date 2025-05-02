from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import UserProfile

def user(request):
    return render(request, 'user/login.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('aviso_list'))
            else:
                messages.error(request, 'Senha incorreta.')
        except User.DoesNotExist:
            messages.error(request, 'Email não encontrado.')

    return render(request, 'user/login.html', {'form_type': 'login'})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
        else:
            return render(request, 'user/login.html', {'form': form, 'show_register': True})
    else:
        form = RegisterForm()
        return render(request, 'user/login.html', {'form': form, 'show_register': True})

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('login')
