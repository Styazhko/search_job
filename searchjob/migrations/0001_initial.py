# Generated by Django 4.1 on 2022-09-16 09:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название компании')),
                ('location', models.CharField(max_length=64, verbose_name='Местоположение')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company/%Y-%m-%d/', verbose_name='Изображение')),
                ('description', models.TextField(verbose_name='Информация о компании')),
                ('employee_count', models.IntegerField(verbose_name='Количество сотрудников')),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Компании',
                'verbose_name_plural': 'Компании',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64, unique=True)),
                ('title', models.CharField(max_length=64)),
                ('picture', models.ImageField(upload_to='specialty/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Специальности',
                'verbose_name_plural': 'Специальности',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_vacancy', models.CharField(max_length=64, verbose_name='Название вакансии')),
                ('skills', models.CharField(max_length=64, verbose_name='Требуемые навыки')),
                ('description', models.TextField(verbose_name='Описание вакансии')),
                ('salary_min', models.PositiveIntegerField(verbose_name='Зарплата от')),
                ('salary_max', models.PositiveIntegerField(verbose_name='Зарплата до')),
                ('published_at', models.DateField(default=datetime.date.today, verbose_name='Дата изменения')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='searchjob.company', verbose_name='Компания')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='searchjob.specialty', verbose_name='Специализация')),
            ],
            options={
                'verbose_name': 'Вакансии',
                'verbose_name_plural': 'Вакансии',
                'ordering': ['-published_at', 'company'],
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('written_username', models.CharField(max_length=64, verbose_name='Ваше имя')),
                ('written_phone', models.CharField(max_length=11, verbose_name='Номер телефона')),
                ('written_cover_letter', models.TextField(verbose_name='Сообщение')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='response', to=settings.AUTH_USER_MODEL)),
                ('vacancy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='response', to='searchjob.vacancy')),
            ],
            options={
                'verbose_name': 'Отклики',
                'verbose_name_plural': 'Отклики',
                'ordering': ['user'],
            },
        ),
    ]
