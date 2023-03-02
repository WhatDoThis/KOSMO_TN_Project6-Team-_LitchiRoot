from django.contrib import admin
from .models import Seeker, Company, Apply, Recruitment

# Register your models here.

Models = [Seeker, Company, Apply, Recruitment]

for model in Models:
    admin.site.register(model)