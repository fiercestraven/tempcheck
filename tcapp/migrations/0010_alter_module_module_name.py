# Generated by Django 4.1.3 on 2022-11-29 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcapp', '0009_alter_lecture_lecture_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='module_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
