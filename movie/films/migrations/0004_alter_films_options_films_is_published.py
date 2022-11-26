# Generated by Django 4.1.3 on 2022-11-10 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_alter_films_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='films',
            options={'ordering': ['id'], 'verbose_name': 'Фильм', 'verbose_name_plural': 'Фильмы'},
        ),
        migrations.AddField(
            model_name='films',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]