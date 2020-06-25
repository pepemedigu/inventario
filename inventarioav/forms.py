from django import forms
from .models import Equipo
from django.forms import CharField, ModelForm, SlugField
from django.core import validators
from django.utils.translation import gettext_lazy as _


class EquipoForm(ModelForm):

    class Meta:
        model = Equipo
        fields = ('modelo', 'numero_serie', 'numero_inventario', 'codigo_suministro', 'fecha_suministro', 'fecha_instalacion', 'fecha_fin_garantia',  'comentarios')
        #comentarios = forms.CharField(widget=forms.Textarea, required=False, max_length=400)
        #numero_serie = forms.CharField(widget=forms.CharField(), required=True, max_length=50)
        #numero_inventario = forms.CharField(widget=forms.CharField(), required=True, max_length=50)

        help_texts = {
            'modelo': _('Debe seleccionar modelo'),
            'numero_serie': _('Debe introducir nº de serie'),
        }
