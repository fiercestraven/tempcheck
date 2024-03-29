# Generated by Django 4.1.2 on 2022-10-08 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_name', models.CharField(max_length=200)),
                ('lecture_description', models.TextField(default='')),
                ('lecture_date', models.DateTimeField(verbose_name='date of lecture')),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('lecturer_password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_name', models.CharField(max_length=200)),
                ('module_description', models.TextField(default='')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tcapp.lecturer')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('student_password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tcapp.module')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tcapp.student')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tcapp.lecture')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tcapp.student')),
            ],
        ),
        migrations.CreateModel(
            name='Ping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ping_date', models.DateTimeField(verbose_name='date and time of ping')),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tcapp.lecture')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tcapp.student')),
            ],
        ),
        migrations.AddField(
            model_name='lecture',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tcapp.module'),
        ),
    ]
