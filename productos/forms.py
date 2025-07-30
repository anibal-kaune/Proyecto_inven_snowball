from django import forms
from .models import Producto, Marca, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }