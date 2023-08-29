from django import forms
from .models import *
from django.utils.functional import cached_property


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

class ProjectMaterialSetFormSet(forms.BaseModelFormSet):

    # Research what this does
    extra = 0
    can_delete = True
    can_order = False
    max_num = 1000
    validate_max = False

    # If you want to enforce each project to have at least
    # one material, set validate_min to True. Research this.
    min_num = 1
    validate_min = False
    absolute_max = 1000
    can_delete_extra = True
    renderer = forms.renderers.get_default_renderer()

    model = ProjectMaterialSet

    #Research why do I need to nest classes
    class ProjectMaterialSetForm(forms.ModelForm):

        # Add an extra name field to help form rendering
        material_name = forms.CharField(max_length=200, required=False)
        class Meta:
            model = ProjectMaterialSet
            fields = ['material', 'material_qty']
    
    # Research this
    form = ProjectMaterialSetForm

    # ProjectForm is like another management form for the formset: 
    # rendered, validated and saved together with formset. Research this.
    class ProjectForm(forms.ModelForm):
        class Meta:
            model = Project
            fields = ['name', 'description']

            widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter the project name'}),
                'description': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter the project description', 'rows': '5'}),
            }

    @cached_property
    def project_form(self):
        if self.is_bound:
            form = self.ProjectForm(self.data, self.files, prefix=self.prefix)
            form.full_clean()
        else:
            form = self.ProjectForm(prefix=self.prefix)
        return form

    def clean(self):
        super().clean()
        if not self.project_form.is_valid():
            raise forms.ValidationError('Project form invalid')

    def save(self, user):
        project = self.project_form.save(commit=False)
        project.created_by = user
        project.save()

        for form in self:
            form.instance.project = project
            
        return super(ProjectMaterialSetFormSet, self).save()
        # return project if you want the instance for further operation,
        # but just don't forget to call super().save()

    def get_queryset(self):
        # Override get_queryset to return none if not specified. 
        # Otherwise, it just returns all. 
        if not hasattr(self, '_queryset'):
            if self.queryset is not None:
                qs = self.queryset
            else:
                qs = self.model.objects.none()
            if not qs.ordered:
                qs = qs.order_by(self.model._meta.pk.name)
            self._queryset = qs
        return self._queryset
