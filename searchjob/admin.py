from django.contrib import admin

from .models import *

admin.site.register(Vacancy)
admin.site.register(Specialty)
admin.site.register(Company)
admin.site.register(Response)