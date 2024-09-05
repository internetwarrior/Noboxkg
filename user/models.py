from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from post.models import Post





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


class UserSession(models.Model):
    ip = models.GenericIPAddressField()
    visited_posts = models.ManyToManyField(Post, blank=True)  # Assuming Post is the name of your post model
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, default=None)

    def __str__(self):
        return f"Session ID: {self.id} - IP: {self.ip}"
