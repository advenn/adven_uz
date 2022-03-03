"""adven URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from ttsongrec.views import homepage, get_link, test, download_file, download_music, direct_from_url, direct
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
urlpatterns = [
    path('', homepage, name='main'),
    path('admin/', admin.site.urls),
    # path('recognizer/', include('adven.ttsongrec.urls')),
    # path('r/', include('adven.ttsongrec.urls')),
    path('link/', get_link, name='form'),
    path('test/', test, name='test'),
    path('download/<str:filepath>', download_file, name='download'),
    path('download_music/<music>', download_music, name='download_music'),
    path('download_music/', test),
    path('download/', test),
    re_path(r'^favicon\.ico$', favicon_view),
    # path('getmusic/', include('adven.ttsongrec.urls'), name='rest'),
    path('video/<str:data>', direct_from_url, name='direct_url'),
    re_path(r'^video/http', direct, name='direct')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG or not settings.DEBUG:
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'ttsongrec.views.page404'
