from django.contrib import admin
from .models import Attandance, Student, Course

# Register your models here.
admin.site.register([Attandance, Student, Course])
