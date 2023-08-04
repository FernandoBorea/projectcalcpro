from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{self.username}'


class Material(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    descrption = models.CharField(max_length=3000, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=20)
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='materials')


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000, blank=True)
    materials = models.ManyToManyField(to=Material, on_delete=models.CASCADE, related_name='projects')
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_created=True)
    