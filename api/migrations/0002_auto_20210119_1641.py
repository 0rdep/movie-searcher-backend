# Generated by Django 3.1.5 on 2021-01-19 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='content_rating',
            field=models.CharField(max_length=255),
        ),
    ]
