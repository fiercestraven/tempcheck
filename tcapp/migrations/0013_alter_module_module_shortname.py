# Generated by Django 4.1.3 on 2022-12-05 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcapp', '0012_module_module_shortname_alter_module_module_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='module_shortname',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
