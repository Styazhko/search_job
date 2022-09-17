from django.test import TestCase
from django.urls import reverse

from account.models import User
from searchjob.models import Vacancy, Specialty, Company


class VacanciesListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_vacancies = 7
        specialty = Specialty.objects.create(code='backend', title='Бэкенд')
        for vacancy_num in range(number_of_vacancies):
            Vacancy.objects.create(
                title_vacancy='Python developer %s' % vacancy_num,
                skills='Бэкенд %s' % vacancy_num,
                description='Описание %s' % vacancy_num,
                salary_min=100,
                salary_max=150,
                specialty=specialty,
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/vacancies/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('vacancies'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('vacancies'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'vacancies.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('vacancies'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['vacancies']) == 5)

    def test_lists_all_authors(self):
        resp = self.client.get(reverse('vacancies') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['vacancies']) == 2)


class VacancyInstancesByUserListViewTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='test@test.ru',
        )
        test_user.save()
        specialty = Specialty.objects.create(
            code='backend',
            title='Бэкенд',
        )
        test_company = Company.objects.create(
            name='Simbirsoft',
            location='Ульяновск',
            description='Описание',
            employee_count=1500,
            owner=test_user
        )
        number_of_vacancies=30
        for vacancy_num in range(number_of_vacancies):
            Vacancy.objects.create(
                title_vacancy='Python developer %s' % vacancy_num,
                skills='Бэкенд %s' % vacancy_num,
                description='Описание %s' % vacancy_num,
                salary_min=100,
                salary_max=150,
                specialty=specialty,
                company=test_company,
            )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('my_vacancies'))
        # Проверка, что произойдет редирект, если not user.is_authenticated
        self.assertRedirects(resp, '/login/?next=/account/myvacancies/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(
            email='test@test.ru',
            password='12345',
        )
        resp = self.client.get(reverse('my_vacancies'))
        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test@test.ru')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)
        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'my_vacancies.html')