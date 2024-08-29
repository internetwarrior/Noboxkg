from django.contrib import admin
from .models import CustomUser,TelegramProfile

admin.site.register(CustomUser)
admin.site.register(TelegramProfile)
# Register your models here.
