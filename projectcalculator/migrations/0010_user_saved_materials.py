# Generated by Django 4.2.4 on 2023-12-13 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectcalculator', '0009_project_materials'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='saved_materials',
            field=models.ManyToManyField(blank=True, related_name='saved_by', to='projectcalculator.material'),
        ),
    ]