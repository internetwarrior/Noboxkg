from django.urls import path
from .views import home_view,post_detail,tiktok,privacy

urlpatterns = [
    path('privacy/',privacy,name = "privacy_page"),
    path('tiktok/',tiktok,name = "tiktok"),
    path('', home_view, name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail')
    ]
