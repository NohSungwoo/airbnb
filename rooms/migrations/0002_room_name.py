# Generated by Django 5.1 on 2024-08-21 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="name",
            field=models.CharField(default="", max_length=180),
        ),
    ]
