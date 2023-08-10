from django import forms
from .models import *


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = ('name', 'description', 'unit', 'price')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the material name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the material description', 'rows': '3'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the material price per unit'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the material unit of measure'})
        }