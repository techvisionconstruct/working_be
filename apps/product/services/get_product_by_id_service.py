from typing import Optional, Tuple

from apps.product.models import Product
from apps.user.models import User


def get_product_by_id_service(
    product_id: str, user: User
) -> Tuple[Optional[Product], Optional[str]]:
    try:
        # Try to find the product
        product = Product.objects.filter(id=product_id).first()

        # If product doesn't exist
        if not product:
            return None, "Product not found"

        # Check if user has access (user is the creator of the product)
        if product.created_by != user:
            return None, "You don't have permission to access this product"

        return product, None
    except Exception as e:
        return None, f"Error retrieving product: {str(e)}"
