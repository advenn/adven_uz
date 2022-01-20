from django.urls import path, include
from .views import recognizer

urlpatterns = [
    path('', recognizer, name='recognizer')
]