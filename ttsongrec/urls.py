from django.urls import path, include
from django.conf import settings
from .views import recognizer
from django.conf.urls.static import static

urlpatterns = [
    path('', recognizer, name='recognizer')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)