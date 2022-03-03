from django.contrib import admin

from .models import Music, Video, URL, Recognized

variables = """ID
Title
Video_id
Url
Thumb
Video
Date
""".splitlines()
variables = [x.lower() for x in variables]


# Register your models here.
def show(model):
    class Show(admin.ModelAdmin):
        list_display = [field.name for field in model._meta.get_fields()] if model != Video else variables

    return Show


admin.site.register(Music, show(Music))
admin.site.register(Video, show(Video))
admin.site.register(URL, show(URL))
admin.site.register(Recognized, show(Recognized))
