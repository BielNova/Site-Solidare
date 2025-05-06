from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist 
from core.professor.models import Professor          
from .forms import RegisterForm 


def user(request):
    return render(request, 'user/login.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            
            is_professor = False
            try:
                if hasattr(request.user, "professor") and isinstance(request.user.professor, Professor):
                    is_professor = True
            except ObjectDoesNotExist:
                pass
            except AttributeError:
                pass

            if is_professor:
                messages.success(request, f"Bem-vindo(a) de volta, Professor(a) {user.username}!")
                return redirect(reverse("professor:dashboard_professor"))
            else:
                messages.success(request, f"Login bem-sucedido, {user.username}!")
                return redirect(reverse("avisos:aviso_list"))
        else:
            messages.error(request, "Credenciais inválidas.")
    return render(request, "user/login.html", {"form_type": "login"})



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
            
            return render(request, 'user/login.html', {'form': form, 'show_register': True})
    else:
        form = RegisterForm()
    
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('home')
