# Generated by Django 3.1.5 on 2021-01-20 05:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20210119_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='user_favorites',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]