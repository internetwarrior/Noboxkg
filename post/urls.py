from django.urls import path
from .views import home_view,post_detail
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home_view, name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)