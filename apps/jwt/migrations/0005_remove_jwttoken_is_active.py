# Generated by Django 5.2 on 2025-04-30 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jwt", "0004_remove_jwttoken_created_by_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="jwttoken",
            name="is_active",
        ),
    ]
