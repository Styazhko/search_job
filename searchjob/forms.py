from django import forms

from .models import Response, Company, Vacancy


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = (
            'written_username',
            'written_phone',
            'written_cover_letter',
        )


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