from django.contrib import admin
from .models import CustomUser,TelegramProfile,UserSession

admin.site.register(CustomUser)
admin.site.register(TelegramProfile)
admin.site.register(UserSession)
# Register your models here.
