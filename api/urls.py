# myapp/urls.py
from django.urls import path
from .views import tuk_tuk_view

urlpatterns = [
    path('tuktuk', tuk_tuk_view, name='tuk_tuk_view'),
]
