from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),  # Use an empty string for the root URL
    path('', include('post.urls')),  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
