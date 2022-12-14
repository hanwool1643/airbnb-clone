# Generated by Django 4.1.3 on 2022-12-04 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "experiences",
            "0003_alter_experience_categories_alter_experience_host_and_more",
        ),
        ("medias", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="experience",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="experiences.experience",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="experience",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="videos",
                to="experiences.experience",
            ),
        ),
    ]
