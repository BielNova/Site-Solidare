from django import forms

class ContatoForm(forms.Form):
    nome = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    assunto = forms.CharField(max_length=200, required=True)
    mensagem = forms.CharField(widget=forms.Textarea, required=True)
