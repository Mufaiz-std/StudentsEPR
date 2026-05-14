from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)
    
    class Meta:
        db_table = 'CUSTOM_USER_TABLE'
