from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    phone_number = models.CharField(max_length=15, unique=False, verbose_name="Номер телефона",default='default_value',)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set')
    telegram_profile = models.OneToOneField('TelegramProfile', on_delete=models.CASCADE, null=True, blank=True)



class TelegramProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.username or self.first_name} ({self.user.username})"