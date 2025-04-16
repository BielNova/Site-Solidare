from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Aviso

class AvisoListView(ListView):
    model = Aviso
    template_name = 'avisos/aviso_list.html'
    context_object_name = 'avisos'

class AvisoDetailView(DetailView):
    model = Aviso
    template_name = 'avisos/aviso_detail.html'
    context_object_name = 'aviso'

class AvisoCreateView(CreateView):
    model = Aviso
    template_name = 'avisos/aviso_form.html'
    fields = ['titulo', 'conteudo', 'categoria', 'data_expiracao', 'anexo']
