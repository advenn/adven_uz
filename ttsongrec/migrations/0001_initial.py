# Generated by Django 4.0.1 on 2022-01-09 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Name')),
                ('link', models.URLField(blank=True, null=True, verbose_name='link of the song')),
                ('file', models.FileField(null=True, upload_to='media/music/', verbose_name='file')),
                ('artist', models.CharField(blank=True, max_length=300, null=True, verbose_name='artist')),
                ('album', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recognized',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(blank=True, max_length=300, null=True, verbose_name='track artist')),
                ('album', models.CharField(blank=True, max_length=200, null=True, verbose_name='track album')),
                ('name', models.CharField(blank=True, max_length=300, null=True, verbose_name='track name')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='media/cover/', verbose_name='cover')),
            ],
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500, verbose_name='Link to track')),
                ('platform_long', models.CharField(max_length=10, verbose_name='Long name of platform')),
                ('platform_short', models.CharField(max_length=2, verbose_name='Short name of platform')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('video_id', models.CharField(blank=True, max_length=30, null=True)),
                ('thumb', models.ImageField(blank=True, null=True, upload_to='media/images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ttsongrec.url')),
            ],
        ),
    ]
