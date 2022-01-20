from django.contrib import admin

from .models import Music, Video, URL, Recognized

# Register your models here.
admin.site.register(Music)
admin.site.register(Video)
admin.site.register(URL)
admin.site.register(Recognized)
