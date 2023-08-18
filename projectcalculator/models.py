from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    # For a default one-to-many, this is not ideal, but will enable multiple users
    # to track a single project on future versions
    saved_projects = models.ManyToManyField(to='Project', related_name='saved_by', blank=True)

    def __str__(self):
        return f'{self.username}'


class Material(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000, blank=True)
    unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='materials')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} (${self.price}/{self.unit})'


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000, blank=True)
    materials = models.ManyToManyField(to=Material, through='ProjectMaterialSet', related_name='projects')
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

class ProjectMaterialSet(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    material = models.ForeignKey(to=Material, on_delete=models.CASCADE)
    material_qty = models.PositiveIntegerField(default=1)

