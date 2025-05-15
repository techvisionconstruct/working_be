from typing import Optional, Tuple

from apps.product.models import Product
from apps.user.models import User


def delete_product_service(product_id: str, user: User) -> Tuple[bool, Optional[str]]:
    try:
        # Check if the product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return False, f"Product with ID {product_id} not found."

        # Check permissions
        if product.created_by != user and not user.is_staff:
            return False, "You don't have permission to delete this product"

        product.delete()
        return True, None
    except Exception as e:
        return False, f"Error deleting product: {str(e)}"
