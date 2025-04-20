from django.shortcuts import render


# Create your views here.
# minhaapp/views.py

def user(request):
    return render(request, 'user/login.html')
