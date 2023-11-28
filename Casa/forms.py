from django import forms
from .models import Casa , Reserva


class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = ['endereco', 'num_quarto', 'preco_total', 'num_banheiro', 'descricao','area','imagem']

    def save(self, commit=True, user=None):
        instance = super(CasaForm, self).save(commit=False)
        if user:
            instance.usuario = user
        if commit:
            instance.save()
        return instance
    
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data_final']
        widgets = {'data_final': forms.DateInput(attrs={'type': 'date'})}