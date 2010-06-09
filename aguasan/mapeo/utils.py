from django import forms
from django.conf import settings

class MontoField(forms.FloatField):
    '''FormField para el campo monto'''
    def clean(self, value):
        value = value.replace(settings.THOUSAND_SEPARATOR, '')
        try:
            return float(value)
        except:
            raise forms.ValidationError("Introduzca un numero")
