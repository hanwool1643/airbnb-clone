# Generated by Django 4.1.3 on 2023-01-15 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0005_alter_room_amenities_alter_room_categories_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room",
            old_name="categories",
            new_name="category",
        ),
    ]