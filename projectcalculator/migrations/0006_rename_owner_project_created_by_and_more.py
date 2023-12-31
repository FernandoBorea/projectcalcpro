# Generated by Django 4.2.4 on 2023-08-12 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectcalculator', '0005_material_created_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='owner',
            new_name='created_by',
        ),
        migrations.AlterField(
            model_name='material',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
