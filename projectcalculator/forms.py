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


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the project description', 'rows': '5'})
        }

    def __init__(self, *args, **kwargs):

        # Store the user object and materials QuerySet
        self.user = kwargs.pop('user') if 'user' in kwargs else None
        self.materials = Material.objects.filter(created_by=self.user) if self.user is not None else None # This is a QuerySet

        # Call parent __init__ method, which we are modifying
        super(ProjectForm, self).__init__(*args, **kwargs)

        # Somehow create a set of forms, one for each material
            # Perhaps using formsets is the ideal solution, however, I keep finding
            # myself going to the route of a dict with forms and adding them as I
            # iterate over the materials query set. 

            # Since formsets are a thing, I'm pretty sure I can somehow create a batch
            # of forms (probably the extra argument is the key here), to then somehow
            # add the material_id to each of them.


class ProjectMaterialSetForm(forms.ModelForm):

    class Meta:
        model = ProjectMaterialSet
        fields = ('material', 'material_qty')

        material = forms.ModelMultipleChoiceField(queryset=None)
        
        widgets = {
            'material': forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}),
            'material_qty': forms.NumberInput(attrs={'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        material_id = kwargs.pop('material_id') if 'material_id' in kwargs else None
        super(ProjectMaterialSetForm, self).__init__(*args, **kwargs)
        self.fields['materials'].queryset = Material.objects.filter(pk=material_id)


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
#         self.user = kwargs.pop('user') if 'user' in kwargs else None

#         # Unsure what this does, will research
#         super(ProjectForm, self).__init__(*args, **kwargs)

#         # Adding queryset to materials field
#         if self.user != None:
#             self.fields['materials'].queryset = Material.objects.filter(created_by=self.user)