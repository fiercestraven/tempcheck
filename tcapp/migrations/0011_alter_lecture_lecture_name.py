# Generated by Django 4.1.3 on 2022-11-29 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcapp', '0010_alter_module_module_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='lecture_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
