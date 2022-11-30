# Generated by Django 4.1.3 on 2022-11-30 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0015_alter_comments_options_alter_films_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='films',
            name='genre',
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(auto_created=True),
        ),
        migrations.AddField(
            model_name='films',
            name='genre',
            field=models.ManyToManyField(related_name='films', to='films.genre'),
        ),
    ]
