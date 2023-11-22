from django import forms
from .models import Mascota


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'edad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre de la mascota'}),
            'especie': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Especie de la mascota'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Edad de la mascota'}),
        }