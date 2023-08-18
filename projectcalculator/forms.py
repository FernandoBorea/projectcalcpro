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


# class ProjectForm(forms.ModelForm):

#     class Meta:
#         model = Project
#         fields = ('name', 'description', 'materials')

#         materials = forms.ModelMultipleChoiceField(queryset=None)

#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the project name'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the project description', 'rows': '5'}),
#             'materials': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
#         }

#     def __init__(self, *args, **kwargs):

#         # Store the request object
#         self.request = kwargs.pop('request') if 'request' in kwargs else None

#         # Unsure what this does, will research
#         super(ProjectForm, self).__init__(*args, **kwargs)

#         # Adding queryset to materials field
#         if self.request != None:
#             self.fields['materials'].queryset = Material.objects.filter(created_by=self.request.user)