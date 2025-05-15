from django.core.management.base import BaseCommand
from apps.product.models import Product


class Command(BaseCommand):
    help = 'Updates the source_platform field to "Home Depot" for all products where it is currently null or empty.'

    def handle(self, *args, **options):
        products_to_update = Product.objects.filter(
            source_platform__isnull=True
        ) | Product.objects.filter(source_platform="")

        updated_count = 0
        for product in products_to_update:
            product.source_platform = "Home Depot"
            product.save(update_fields=["source_platform"])
            updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} products to have "Home Depot" as source_platform.'
            )
        )

        if updated_count == 0:
            total_products = Product.objects.count()
            null_platform_products = Product.objects.filter(
                source_platform__isnull=True
            ).count()
            empty_platform_products = Product.objects.filter(source_platform="").count()

            self.stdout.write(self.style.WARNING("No products needed an update."))
            self.stdout.write(f"Total products: {total_products}")
            self.stdout.write(
                f"Products with null source_platform: {null_platform_products}"
            )
            self.stdout.write(
                f"Products with empty string source_platform: {empty_platform_products}"
            )
