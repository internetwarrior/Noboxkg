from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    phone_number = models.CharField(max_length=15, unique=False, verbose_name="Номер телефона",default='default_value',)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set')
