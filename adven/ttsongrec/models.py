from django.db import models


# Create your models here.
from django.urls import reverse


class URL(models.Model):
    url = models.URLField(verbose_name='Link to track', max_length=500)
    platform_long = models.CharField(max_length=10, verbose_name='Long name of platform')
    platform_short = models.CharField(max_length=2, verbose_name='Short name of platform')

    def __str__(self):
        return self.url


class Video(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=30, null=True, blank=True)
    url = models.ForeignKey(to=URL, on_delete=models.PROTECT)
    thumb = models.ImageField(upload_to='static/images/', null=True, blank=True)
    video = models.FileField(blank=True, null=True, upload_to='media')
    date = models.DateTimeField(auto_now_add=True)
    filesize = models.FloatField(blank=True, null=True, verbose_name='Filesize')
    # length = models.FloatField(blank=True, null=True, verbose_name='Length of video')

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('video/'+self.video_id)


class Recognized(models.Model):
    artist = models.CharField(max_length=300, verbose_name='track artist', null=True, blank=True)
    album = models.CharField(max_length=200, verbose_name='track album', null=True, blank=True)
    name = models.CharField(max_length=300, verbose_name='track name', null=True, blank=True)
    cover = models.ImageField(verbose_name='cover', null=True, blank=True, upload_to='media/cover/')

    def __str__(self):
        return self.name


class Music(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200, verbose_name='Name')
    link = models.URLField(null=True, blank=True, verbose_name='link of the song')
    file = models.FileField(upload_to='media/music/', verbose_name='file', null=True)
    artist = models.CharField(max_length=300, verbose_name='artist', null=True, blank=True)
    album = models.CharField(max_length=200, null=True, blank=True)
    filesize = models.FloatField(blank=True, null=True, verbose_name='Filesize')

    def __str__(self):
        return self.name

    # class Meta:
    #     model_name = "Music"


