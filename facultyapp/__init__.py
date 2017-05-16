from django.db import models
from django.contrib.auth.models import User

pan_number = models.CharField('PAN Number',max_length=10, blank=True, null=True)
pan_number.contribute_to_class(User, 'pan_number')

default_app_config = 'facultyapp.apps.FacultyAppConfig'

