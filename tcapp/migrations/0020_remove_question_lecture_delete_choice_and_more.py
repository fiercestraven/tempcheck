# Generated by Django 4.1.3 on 2023-03-25 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tcapp', '0019_reset_instructor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='lecture',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
