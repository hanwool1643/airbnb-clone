# Generated by Django 4.1.3 on 2023-01-15 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0002_alter_category_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="kind",
            field=models.CharField(
                choices=[("rooms", "Rooms"), ("experiences", "Experiences")],
                max_length=15,
            ),
        ),
    ]
