# Create your models here.
from django.db import models

class SampleUser(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    