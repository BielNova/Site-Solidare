from django import forms
from .models import Aluno, Frequencia # Adicionando Frequencia
from core.avisos.models import Aviso # Importando o modelo Aviso do app core.avisos

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome_completo", "matricula"]
        widgets = {
            "nome_completo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome completo do aluno"}),
            "matricula": forms.TextInput(attrs={"class": "form-control", "placeholder": "Matrícula do aluno"}),
        }

class AvisoForm(forms.ModelForm):
    class Meta:
        model = Aviso
        fields = ["titulo", "conteudo", "categoria", "data_expiracao", "anexo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título do aviso"}),
            "conteudo": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Conteúdo do aviso"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "data_expiracao": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "anexo": forms.FileInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "data_expiracao": "(Opcional)",
            "anexo": "(Opcional)"
        }

class FrequenciaForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        label="Data da Frequência"
    )
    class Meta:
        model = Frequencia
        fields = ["aluno", "data", "presente", "observacao"]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-select"}),
            "presente": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "observacao": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Observações (opcional)"}),
        }

    def __init__(self, *args, **kwargs):
        professor = kwargs.pop("professor", None)
        super().__init__(*args, **kwargs)
        if professor:
            # Filtra os alunos para mostrar apenas os cadastrados pelo professor logado
            self.fields["aluno"].queryset = Aluno.objects.filter(cadastrado_por=professor)

class FrequenciaLoteForm(forms.Form):
    data = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        label="Data da Frequência"
    )
    # Este formulário será populado dinamicamente na view com os alunos do professor
    # Exemplo: aluno_1_presente = forms.BooleanField(required=False, label="Aluno 1")
    #          aluno_1_observacao = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        professor = kwargs.pop("professor", None)
        super().__init__(*args, **kwargs)
        if professor:
            alunos_do_professor = Aluno.objects.filter(cadastrado_por=professor).order_by("nome_completo")
            for aluno in alunos_do_professor:
                self.fields[f"aluno_{aluno.id}_presente"] = forms.BooleanField(
                    required=False, 
                    label=aluno.nome_completo,
                    widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
                )
                self.fields[f"aluno_{aluno.id}_observacao"] = forms.CharField(
                    widget=forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 1, "placeholder": "Obs."}),
                    required=False,
                    label=f"Observação para {aluno.nome_completo}"
                )

