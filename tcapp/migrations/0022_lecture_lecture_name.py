# Generated by Django 4.1.3 on 2023-04-23 20:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tcapp", "0021_rename_lecture_name_lecture_lecture_shortname"),
    ]

    operations = [
        migrations.AddField(
            model_name="lecture",
            name="lecture_name",
            field=models.CharField(default="", max_length=200),
        ),
    ]
