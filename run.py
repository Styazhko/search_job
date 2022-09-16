import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

from searchjob.models import Specialty
from conf import settings
import data

if __name__ == '__main__':
    for spec in data.specialties:
        specialty = Specialty(code=spec['code'],
                              title=spec['title'],
                              picture=f'{settings.MEDIA_SPECIALITY_IMAGE_DIR}/specty_{spec["code"]}.png')
        specialty.save()