# Generated by Django 4.2.8 on 2025-01-16 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0011_user_conversation_list"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="Conversation_List",
        ),
    ]
