# Generated by Django 5.1 on 2024-08-24 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("direct_messages", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="ChattingRoom",
            new_name="room",
        ),
    ]
