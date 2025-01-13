from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comentario

class PredictForm(forms.Form):
    bedrooms = forms.IntegerField(label="Habitaciones",
                                  required=True,
                                  initial=3)
    bathrooms = forms.FloatField(label="Baños",
                                 required=True,
                                 initial=3)
    sqft_living = forms.IntegerField(label="Área habitable (sqft)",
                                     required=True,
                                     initial=1300)
    sqft_lot = forms.IntegerField(label="Área del lote (sqft)",
                                  required=True,
                                  initial=15000)
    floors = forms.FloatField(label="Pisos",
                              required=True,
                              initial=1)
    waterfront = forms.ChoiceField(
        choices=[(0, 'No'), (1, 'Sí')],
        label="Frente al agua",
        required=True,
        initial=1
    )
    view = forms.IntegerField(label="Vista (0 a 4)",
                              required=True,
                              min_value=0,
                              max_value=4,
                              initial=3)
    condition = forms.IntegerField(label="Condición (1 a 5)",
                                   required=True,
                                   min_value=1,
                                   max_value=5,
                                   initial=4)
    grade = forms.IntegerField(label="Calidad (1 a 13)",
                               required=True,
                               min_value=1,
                               max_value=13,
                               initial=7
                               )
    sqft_above = forms.IntegerField(label="Área sobre el suelo (sqft)",
                                    required=True,
                                    initial=20)
    sqft_basement = forms.IntegerField(label="Área del sótano (sqft)", 
                                       required=True,
                                       initial=0)
    yr_built = forms.IntegerField(label="Año de construcción",
                                  required=True,
                                  initial=1999)
    yr_renovated = forms.IntegerField(label="Año de renovación",
                                      required=False,
                                      initial=0)
    zipcode = forms.IntegerField(label="Código postal",
                                 required=True,
                                 initial=98199)

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Requerido. Ingresa tu nombre.'
    )
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Requerido. Ingresa tus apellidos.'
    )
    email = forms.EmailField(
        required=True, help_text='Requerido. Ingresa un correo electrónico válido.'
    )

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu comentario...'}),
        }
        labels = {
            'texto': 'Tu comentario',
        }