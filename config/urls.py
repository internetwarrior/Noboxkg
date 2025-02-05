from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .views import react_app
urlpatterns = [
    path('superman/', admin.site.urls),
    path('noknok/', react_app, name='noknok'),
    path('', include('user.urls')),
    path('', include('post.urls')),
    path('api_v1/', include('api.urls')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
