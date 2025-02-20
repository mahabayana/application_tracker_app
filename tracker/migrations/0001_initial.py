# Generated by Django 5.1 on 2024-11-04 05:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User_Person",
            fields=[
                ("name", models.CharField(max_length=200)),
                (
                    "email",
                    models.EmailField(
                        max_length=254, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Application",
            fields=[
                ("app_id", models.AutoField(primary_key=True, serialize=False)),
                ("company", models.CharField(max_length=200)),
                ("position", models.CharField(max_length=200)),
                ("date_applied", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Applied", "Applied"),
                            ("Interviewing", "Interviewing"),
                            ("Offer Received", "Offer Received"),
                            ("Rejected", "Rejected"),
                        ],
                        max_length=25,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tracker.user_person",
                    ),
                ),
            ],
        ),
    ]
