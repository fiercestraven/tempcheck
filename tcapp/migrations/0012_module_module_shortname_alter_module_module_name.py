# Generated by Django 4.1.3 on 2022-12-05 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcapp', '0011_alter_lecture_lecture_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='module_shortname',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='module',
            name='module_name',
            field=models.CharField(max_length=200),
        ),
    ]
