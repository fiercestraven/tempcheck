# Generated by Django 4.1.3 on 2023-02-08 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tcapp', '0013_alter_module_module_shortname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='instructor',
            field=models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Threshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yellow_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('orange_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('red_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('instructor', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
