# Generated by Django 4.1.3 on 2023-04-24 05:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tcapp", "0022_lecture_lecture_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lecture",
            name="lecture_name",
            field=models.CharField(max_length=200),
        ),
    ]
