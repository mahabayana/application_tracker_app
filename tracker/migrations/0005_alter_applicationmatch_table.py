# Generated by Django 5.1 on 2024-12-06 02:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0004_applicationmatch"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="applicationmatch",
            table="tracker_applicationmatch",
        ),
    ]
