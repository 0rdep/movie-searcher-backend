# Generated by Django 3.1.5 on 2021-01-18 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('poster', models.CharField(max_length=255)),
                ('content_rating', models.IntegerField()),
                ('duration', models.CharField(max_length=255)),
                ('release_date', models.CharField(max_length=255)),
                ('average_rating', models.FloatField()),
                ('original_title', models.CharField(max_length=255)),
                ('storyline', models.CharField(max_length=255)),
                ('imdb_rating', models.FloatField(max_length=255)),
                ('posterurl', models.CharField(max_length=255)),
                ('actors', models.ManyToManyField(to='api.Actor')),
                ('genres', models.ManyToManyField(to='api.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='api.movie')),
            ],
        ),
    ]
