# Generated by Django 4.1.2 on 2022-10-11 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tcapp', '0003_question_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='lecture',
        ),
        migrations.AddField(
            model_name='question',
            name='lecture',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tcapp.lecture'),
            preserve_default=False,
        ),
    ]
