# Generated by Django 5.2 on 2025-04-30 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jwt", "0003_alter_jwttoken_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="jwttoken",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="jwttoken",
            name="updated_by",
        ),
    ]
