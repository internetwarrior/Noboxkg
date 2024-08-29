from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.conf import settings

class Post(models.Model):
    STATE_CHOICES = [
        ('being_checked', 'На проверке'),
        ('active', 'Активно'),
        ('denied', 'Отклонено'),
        ('archived', 'Архивировано')
    ]

    tags = models.ManyToManyField(Tag)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=250)
    picture = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='being_checked')

    def __str__(self):
        return f"Post ID: {self.id} - {self.description[:20]}"
