# Generated by Django 5.0.3 on 2024-03-19 05:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_album_created_by_alter_photo_album_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
