from django.test import TestCase
import datetime

from searchjob.models import Company, Specialty, Vacancy, Response


class CompanyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Company.objects.create(
            name='Simbirsoft',
            location='Ульяновск',
            description='Описание',
            employee_count=1500,
        )

    def test_create_company(self):
        company = Company.objects.get(id=1)
        self.assertIsInstance(company, Company)

    def test_name(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('name').verbose_name
        max_length = company._meta.get_field('name').max_length
        self.assertEquals(field_label,'Название компании')
        self.assertEquals(max_length, 64)

    def test_location(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('location').verbose_name
        max_length = company._meta.get_field('location').max_length
        self.assertEquals(field_label,'Местоположение')
        self.assertEquals(max_length, 64)

    def test_employee_count(self):
        company = Company.objects.get(id=1)
        employee = company.employee_count
        self.assertIsInstance(employee, int)

    def test_description(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('description').verbose_name
        description_text = company.description
        self.assertEquals(field_label, 'Информация о компании')
        self.assertIsInstance(description_text, str)


class SpecialtyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Specialty.objects.create(
            code='backend',
            title='Бэкенд',
        )

    def test_create_specialty(self):
        specialty = Specialty.objects.get(id=1)
        self.assertIsInstance(specialty, Specialty)

    def test_code(self):
        specialty = Specialty.objects.get(id=1)
        max_length = specialty._meta.get_field('code').max_length
        self.assertEquals(max_length, 64)
        self.assertEquals(specialty.code, 'backend')

    def test_title(self):
        specialty = Specialty.objects.get(id=1)
        max_length = specialty._meta.get_field('title').max_length
        self.assertEquals(max_length, 64)
        self.assertEquals(specialty.title, 'Бэкенд')

class VacancyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        specialty = Specialty.objects.create(
            code='backend',
            title='Бэкенд',
        )
        Vacancy.objects.create(
            title_vacancy='Python developer',
            skills='Бэкенд',
            description='Описание',
            salary_min=100,
            salary_max=150,
            specialty=specialty,
        )

    def test_create_vacancy(self):
        vacancy = Vacancy.objects.get(id=1)
        self.assertIsInstance(vacancy, Vacancy)

    def test_title_vacancy(self):
        vacancy = Vacancy.objects.get(id=1)
        max_length = vacancy._meta.get_field('title_vacancy').max_length
        self.assertEquals(max_length, 64)
        self.assertEquals(vacancy.title_vacancy, 'Python developer')

    def test_skills(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('skills').verbose_name
        max_length = vacancy._meta.get_field('skills').max_length
        self.assertEquals(field_label, 'Требуемые навыки')
        self.assertEquals(max_length, 64)
        self.assertEquals(vacancy.skills, 'Бэкенд')

    def test_description(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание вакансии')
        self.assertEquals(vacancy.description, 'Описание')

    def test_published_at(self):
        vacancy = Vacancy.objects.get(id=1)
        self.assertEquals(vacancy.published_at, datetime.date.today())

    def test_salary(self):
        vacancy = Vacancy.objects.get(id=1)
        self.assertEquals(vacancy.salary_max > vacancy.salary_min, True)

    def test_specialty_id(self):
        vacancy = Vacancy.objects.get(id=1)
        self.assertIsInstance(vacancy.specialty, Specialty)


class ResponseModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Response.objects.create(
            written_username='Николай',
            written_phone='89935830019',
            written_cover_letter='Python Backend - developer',
        )

    def test_written_username(self):
        responce = Response.objects.get(id=1)
        field_label = responce._meta.get_field('written_username').verbose_name
        self.assertEquals(field_label, 'Ваше имя')
        self.assertEquals(responce.written_username, 'Николай')

    def test_written_phone(self):
        responce = Response.objects.get(id=1)
        field_label = responce._meta.get_field('written_phone').verbose_name
        self.assertEquals(field_label, 'Номер телефона')
        self.assertEquals(responce.written_phone, '89935830019')

    def test_written_cover_letter(self):
        responce = Response.objects.get(id=1)
        field_label = responce._meta.get_field('written_cover_letter').verbose_name
        self.assertEquals(field_label, 'Сообщение')
        self.assertEquals(responce.written_cover_letter, 'Python Backend - developer')
