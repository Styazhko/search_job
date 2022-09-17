import datetime

from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название компании')
    location = models.CharField(max_length=64, verbose_name='Местоположение')
    logo = models.ImageField(upload_to='company/%Y-%m-%d/', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Информация о компании')
    employee_count = models.IntegerField(verbose_name='Количество сотрудников')
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='company')

    class Meta:
        verbose_name = 'Компании'
        verbose_name_plural = 'Компании'
        ordering = ['name']

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to='specialty/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Специальности'
        verbose_name_plural = 'Специальности'
        ordering = ['code']

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title_vacancy = models.CharField(max_length=64, verbose_name='Название вакансии')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies', verbose_name='Специализация')
    company = models.ForeignKey(Company,  null=True, on_delete=models.CASCADE, related_name="vacancies", verbose_name='Компания')
    skills = models.CharField(max_length=64, verbose_name='Требуемые навыки')
    description = models.TextField(verbose_name='Описание вакансии')
    salary_min = models.PositiveIntegerField(verbose_name='Зарплата от')
    salary_max = models.PositiveIntegerField(verbose_name='Зарплата до')
    published_at = models.DateField(default=datetime.date.today, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Вакансии'
        verbose_name_plural = 'Вакансии'
        ordering = ['-published_at', 'company']

    def __str__(self):
        return self.title_vacancy



class Response(models.Model):
    written_username = models.CharField(max_length=64, verbose_name='Ваше имя')
    written_phone = models.CharField(max_length=11, verbose_name='Номер телефона')
    written_cover_letter = models.TextField(verbose_name='Сообщение')
    vacancy = models.ForeignKey(Vacancy, null=True, on_delete=models.CASCADE, related_name='response')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='response')

    class Meta:
        verbose_name = 'Отклики'
        verbose_name_plural = 'Отклики'
        ordering = ['user']