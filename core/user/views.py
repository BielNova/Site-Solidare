from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from core.professor.models import Professor, Aluno
from .forms import RegisterForm

UserModel = get_user_model()

def user(request):
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
            except (ObjectDoesNotExist, AttributeError):
                pass

            is_aluno = False
            try:
                aluno = Aluno.objects.filter(user=request.user).first()
                if aluno:
                    is_aluno = True
            except (ObjectDoesNotExist, AttributeError):
                pass

            if is_professor:
                messages.success(request, f"Bem-vindo(a) de volta, Professor(a) {user_to_auth.username}!")
                return redirect(reverse("professor:dashboard_professor"))
            elif is_aluno:
                messages.success(request, f"Bem-vindo(a) de volta, Aluno(a) {user_to_auth.username}!")
                return redirect(reverse("aluno:dashboard_aluno"))
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
            return redirect(reverse('user:login'))
        else:
            return render(request, 'user/login.html', {'form': form, 'show_register': True, 'form_type': 'register'})
    else:
        form = RegisterForm()
    return render(request, 'user/login.html', {'form': form, 'form_type': 'register'})

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    try:
        return redirect(reverse('home:home'))
    except Exception:
        return redirect('/')

