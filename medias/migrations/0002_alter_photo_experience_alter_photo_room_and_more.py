# Generated by Django 5.1 on 2024-08-25 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0003_alter_experience_category_alter_experience_host"),
        ("medias", "0001_initial"),
        ("rooms", "0005_alter_room_amenities_alter_room_categories_and_more"),
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
            model_name="photo",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="rooms.room",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="experience",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="video",
                to="experiences.experience",
            ),
        ),
    ]
