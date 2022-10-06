import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

from searchjob.models import Specialty, Vacancy, Company
from conf import settings
import data

if __name__ == '__main__':

    Specialty.objects.all().delete()
    Company.objects.all().delete()
    Vacancy.objects.all().delete()

    for spec in data.specialties:
        specialty = Specialty(code=spec['code'],
                              title=spec['title'],
                              picture=f'{settings.MEDIA_SPECIALITY_IMAGE_DIR}/specty_{spec["code"]}.png',
                              )
        specialty.save()


    for comp in data.companies:
        company = Company(name=comp['title'],
                          logo=f'{settings.MEDIA_COMPANY_IMAGE_DIR}/logo{comp["id"]}.png',
                          employee_count=int(comp['employee_count']),
                          location=comp['location'],
                          description=comp['description'],
                          )
        company.save()


    for job in data.jobs:
        vacancy = Vacancy(title_vacancy=job['title'],
                          specialty=Specialty.objects.get(code=job['specialty']),
                          company=Company.objects.get(name=job['company']),
                          salary_min=int(job['salary_from']),
                          salary_max=int(job['salary_to']),
                          skills=job['skills'],
                          description=job['description'],
                          )
        vacancy.save()
