from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from core.professor.models import Professor
from .forms import RegisterForm

UserModel = get_user_model()

# É uma boa prática definir o app_name no seu arquivo core/user/urls.py
# Exemplo: app_name = 'user'
# Isso garante que os namespaces funcionem como esperado.

def user(request):
    # Esta view parece ser a que renderiza a página de login/registro inicialmente.
    # O nome da URL para ela é 'user' no seu urls.py.
    return render(request, 'user/login.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "E-mail e senha são obrigatórios.")
            return render(request, "user/login.html", {"form_type": "login"})

        try:
            user_obj_by_email = UserModel.objects.get(email=email)
            user_to_auth = authenticate(request, username=user_obj_by_email.username, password=password)
        except UserModel.DoesNotExist:
            user_to_auth = None

        if user_to_auth is not None:
            login(request, user_to_auth)
            is_professor = False
            try:
                if hasattr(request.user, "professor") and isinstance(request.user.professor, Professor):
                    is_professor = True
            except ObjectDoesNotExist:
                pass
            except AttributeError:
                pass

            if is_professor:
                messages.success(request, f"Bem-vindo(a) de volta, Professor(a) {user_to_auth.username}!")
                return redirect(reverse("professor:dashboard_professor"))
            else:
                messages.success(request, f"Login bem-sucedido, {user_to_auth.username}!")
                return redirect(reverse("avisos:aviso_list"))
        else:
            messages.error(request, "Credenciais inválidas. Verifique seu e-mail e senha.")
            return render(request, "user/login.html", {"form_type": "login"})
    else:
        return render(request, "user/login.html", {"form_type": "login"})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.set_password(form.cleaned_data['password'])
            user_obj.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            # Corrigido para usar o nome da URL 'login' dentro do namespace 'user'
            # Certifique-se que seu core/user/urls.py tem app_name = 'user'
            # ou que foi incluído com namespace 'user' no urls.py principal.
            return redirect(reverse('user:login'))
        else:
            return render(request, 'user/login.html', {'form': form, 'show_register': True, 'form_type': 'register'})
    else:
        form = RegisterForm()
    return render(request, 'user/login.html', {'form': form, 'form_type': 'register'})

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    # Certifique-se que 'home:home' é o nome correto da sua URL da página inicial.
    # Isso requer que a app 'home' tenha um urls.py com app_name = 'home'
    # e uma URL nomeada 'home', ou que seja incluída com namespace 'home'.
    # Se sua home for uma URL global sem namespace, seria apenas reverse('home').
    try:
        return redirect(reverse('home:home'))
    except Exception:
        # Fallback para uma URL raiz ou outra página segura se 'home:home' falhar
        return redirect('/')

