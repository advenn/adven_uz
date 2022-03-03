# Generated by Django 4.0.1 on 2022-01-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttsongrec', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='filesize',
            field=models.FloatField(blank=True, null=True, verbose_name='Filesize'),
        ),
        migrations.AddField(
            model_name='video',
            name='filesize',
            field=models.FloatField(blank=True, null=True, verbose_name='Filesize'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]