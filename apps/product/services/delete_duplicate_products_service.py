from typing import Tuple, Optional
from django.db import transaction
from django.db.models import Count, Min

from apps.product.models import Product
from apps.user.models import User


def delete_duplicate_products_service(user: User) -> Tuple[int, Optional[str]]:
    deleted_count = 0
    try:
        with transaction.atomic():
            # Find item_ids that are duplicated for the current user
            duplicate_item_ids = (
                Product.objects.filter(created_by=user)
                .values("item_id")
                .annotate(count=Count("id"))
                .filter(count__gt=1)
                .values_list("item_id", flat=True)
            )

            if not duplicate_item_ids:
                return 0, "No duplicate products found."

            for item_id in duplicate_item_ids:
                # For each duplicate item_id, find all associated products
                products_to_check = Product.objects.filter(
                    created_by=user, item_id=item_id
                ).order_by("id")

                # The first product in the ordered list is the one to keep
                product_to_keep = products_to_check.first()

                if product_to_keep:
                    # Delete all other products with the same item_id
                    products_to_delete = products_to_check.exclude(
                        id=product_to_keep.id
                    )
                    deleted_count += products_to_delete.count()
                    products_to_delete.delete()

        return deleted_count, None
    except Exception as e:
        return 0, f"An error occurred: {str(e)}"
