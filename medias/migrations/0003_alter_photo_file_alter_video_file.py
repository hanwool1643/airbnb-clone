# Generated by Django 4.1.5 on 2023-02-01 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0002_alter_photo_experience_alter_video_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.URLField(),
        ),
    ]
