# Generated by Django 5.1.1 on 2024-09-17 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_first_name_alter_user_last_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_photo",
            field=models.URLField(blank=True, null=True),
        ),
    ]
