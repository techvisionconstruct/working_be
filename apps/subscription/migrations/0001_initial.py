# Generated by Django 5.2 on 2025-04-29 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.CharField(
                        default="rHebPrDDGc",
                        max_length=10,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("inactive", "Inactive"),
                            ("pending", "Pending"),
                            ("canceled", "Canceled"),
                            ("expired", "Expired"),
                            ("trial", "Trial"),
                        ],
                        default="active",
                        max_length=20,
                    ),
                ),
                (
                    "subscription_type",
                    models.CharField(
                        choices=[
                            ("free", "Free"),
                            ("paid", "Paid"),
                            ("trial", "Trial"),
                            ("gift", "Gift"),
                        ],
                        default="free",
                        max_length=20,
                    ),
                ),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("is_auto_renew", models.BooleanField(default=True)),
                (
                    "payment_method",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("last_payment_date", models.DateTimeField(blank=True, null=True)),
                (
                    "last_payment_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("next_payment_date", models.DateTimeField(blank=True, null=True)),
                (
                    "next_payment_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("inactive", "Inactive"),
                            ("pending", "Pending"),
                            ("canceled", "Canceled"),
                            ("expired", "Expired"),
                            ("trial", "Trial"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Subscription",
                "verbose_name_plural": "Subscriptions",
                "db_table": "subscriptions",
                "ordering": ["-created_at"],
            },
        ),
    ]
