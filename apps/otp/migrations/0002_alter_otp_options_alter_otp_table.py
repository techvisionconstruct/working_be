# Generated by Django 5.2 on 2025-05-12 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("otp", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="otp",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "OTP",
                "verbose_name_plural": "OTPs",
            },
        ),
        migrations.AlterModelTable(
            name="otp",
            table="otps",
        ),
    ]
