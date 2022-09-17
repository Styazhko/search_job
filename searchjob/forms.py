from django import forms
from django.core.exceptions import ValidationError

from .models import Response, Company, Vacancy


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = (
            'written_username',
            'written_phone',
            'written_cover_letter',
        )

    # def clean_written_phone(self):
    #     written_phone = self.cleaned_data['written_phone']
    #     if written_phone != r'^8\d{10}$':
    #         raise ValidationError("Введите номер в формате 8XXXXXXXXXX (X - число от 0 до 9)")
    #     return written_phone

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = (
            'name',
            'location',
            'logo',
            'description',
            'employee_count',
        )


class VacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = (
            'title_vacancy',
            'specialty',
            'skills',
            'description',
            'salary_min',
            'salary_max',
        )

    def clean_salary_max(self):
        salary_max = self.cleaned_data['salary_max']
        salary_min = self.cleaned_data['salary_min']

        if salary_max < salary_min:
            raise ValidationError('Максимальная зарплата должна быть больше минимальной')
        return salary_max