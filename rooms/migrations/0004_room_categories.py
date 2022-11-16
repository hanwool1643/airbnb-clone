# Generated by Django 4.1.3 on 2022-11-16 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
        ("rooms", "0003_alter_amenity_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="categories",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="categories.category",
            ),
        ),
    ]
