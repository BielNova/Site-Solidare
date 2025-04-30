# -*- coding: utf-8 -*-
from django import forms
from .models import Aula, Presenca, Nota
from django.forms import modelformset_factory

# Formulário para criar/editar Aulas
class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        # Corrigido: Removido \
        fields = ["data", "topico", "descricao"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
        }

# Formulário para registrar/editar Notas (pode precisar de ajustes dependendo da UI)
class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        # Corrigido: Removido \
        fields = ["aluno", "atividade", "nota"] # Turma será definida na view
        # Pode ser útil usar widgets específicos ou ocultar o aluno se o form for por aluno

# FormSet para Presença (usado na view registrar_presenca)
# A definição do FormSet é feita diretamente na view usando modelformset_factory
# PresencaFormSet = modelformset_factory(Presenca, fields=("status",), extra=0)

# FormSet para Notas (exemplo, pode precisar de customização)
# NotaFormSet = modelformset_factory(Nota, form=NotaForm, extra=0)
# A implementação exata do NotaFormSet pode variar. A view atual não o utiliza completamente.

