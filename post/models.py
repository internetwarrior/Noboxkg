from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    tags = models.ManyToManyField(Tag)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=250)
    contacts = models.IntegerField()
    picture = models.CharField(max_length=255)

    def __str__(self):
        return f"Post ID: {self.id} - {self.description[:20]}"