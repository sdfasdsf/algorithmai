# Generated by Django 4.2.8 on 2025-01-14 03:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AI",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user_question",
                    models.CharField(max_length=200, verbose_name="질문"),
                ),
                (
                    "bot_response",
                    models.TextField(blank=True, null=True, verbose_name="챗봇 응답"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="질문한 시간"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
