# Generated by Django 4.2.8 on 2025-01-24 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0023_remove_article_writer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="total_commentlikes_count",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="writer",
        ),
    ]
