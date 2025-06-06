# processo_seletivo/forms.py

from django import forms
from .models import Inscricao

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = '__all__' # Inclui todos os campos do modelo no formulário

        # Widgets para personalizar o input de alguns campos no HTML
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            # Para campos CharField que armazenam múltiplos valores de forma textual,
            # como 'bens_possuidos', 'costuma_comer', 'vulnerabilidade_territorial',
            # se você quiser que eles sejam checkboxes no formulário, você precisaria
            # ajustar o modelo para armazenar esses valores de forma mais estruturada (ex: ManyToManyField)
            # ou criar campos de formulário personalizados que serializem/deserializem esses dados.
            # Por enquanto, eles serão renderizados como inputs de texto ou selects,
            # dependendo do tipo de campo do modelo.
            # Se você deseja que 'costuma_comer' seja um CheckboxSelectMultiple, você teria que fazer:
            # 'costuma_comer': forms.MultipleChoiceField(
            #     choices=[('arroz', 'Arroz'), ('feijao', 'Feijão')], # << Adicione suas opções aqui
            #     widget=forms.CheckboxSelectMultiple
            # ),
            # E se o campo no modelo for CharField, você precisaria de lógica na view para lidar com a lista de strings.
        }