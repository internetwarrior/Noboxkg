from django.db import models
from django.conf import settings
from django.utils import timezone
class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Post(models.Model):
    STATE_CHOICES = [
        ('being_checked', 'На проверке'),
        ('active', 'Активно'),
        ('denied', 'Отклонено'),
        ('archived', 'Архивировано')
    ]

    tags = models.ManyToManyField(Tag)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    
    picture = models.CharField(default=None, max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='being_checked')
    
    created = models.DateTimeField(default=timezone.now)
    
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Post ID: {self.id} - {self.description[:20]}"