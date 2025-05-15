import requests
import csv
import os
from typing import Optional, Tuple, List
from decimal import Decimal
from django.utils import timezone

from config.constants import BIGBOX_API_KEY, BIGBIX_API_URL
from apps.product.models import Product
from apps.user.models import User
from apps.user.choices import UserRole


def admin_search_home_depot_products_service(
    search_term: str, sort_by: str, user: User
) -> Tuple[Optional[List[Product]], Optional[str]]:
    # Check if user has admin privileges
    if user.role != UserRole.ADMIN and not user.is_superuser:
        return (
            None,
            "Permission denied: Only administrators can search Home Depot products",
        )

    try:
        # Always use lowercase for search_term
        search_term_lc = search_term.lower()

        # Set up the request parameters
        params = {
            "api_key": BIGBOX_API_KEY,
            "search_term": search_term_lc,
            "type": "search",
            "sort_by": sort_by,
            "output": "csv",
            "csv_fields": "request.search_term,search_results.product.title,search_results.product.item_id,search_results.product.link,search_results.product.primary_image,search_results.product.rating,search_results.product.ratings_total,search_results.offers.primary.price,search_results.offers.primary.currency",
        }

        # Make the HTTP GET request to BigBox API
        api_result = requests.get(BIGBIX_API_URL, params)

        if api_result.status_code != 200:
            return (
                None,
                f"API request failed with status code: {api_result.status_code}",
            )

        # ... existing code ...

        # Prepare directory and file path for saving CSV
        base_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
            ),
            ".csv",
        )
        os.makedirs(base_dir, exist_ok=True)
        csv_file_path = os.path.join(
            base_dir, f"{search_term_lc.replace(' ', '_')}.csv"
        )

        # Parse the new CSV content from API
        decoded_content = api_result.content.decode("utf-8")
        new_rows = list(csv.DictReader(decoded_content.splitlines()))

        # Read existing CSV if it exists
        existing_rows = []
        item_id_to_row = {}
        if os.path.exists(csv_file_path):
            with open(csv_file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                existing_rows = list(reader)
                for row in existing_rows:
                    item_id_to_row[row.get("search_results.product.item_id")] = row

        # Update or add new rows for CSV
        for new_row in new_rows:
            item_id = new_row.get("search_results.product.item_id")
            if item_id in item_id_to_row:
                # Update the existing row with new data
                item_id_to_row[item_id].update(new_row)
            else:
                # Add new product
                existing_rows.append(new_row)
                item_id_to_row[item_id] = new_row

        # Write back to CSV
        if new_rows:
            fieldnames = new_rows[0].keys()
            with open(csv_file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_rows)

        # Save to database: only insert new or update changed products
        products = []
        for row in new_rows:
            item_id = row.get("search_results.product.item_id")
            if not item_id:
                continue
            # Try to find existing product
            try:
                product = Product.objects.get(item_id=item_id)
                # Compare all relevant fields
                changed = (
                    product.search_term != search_term_lc
                    or product.source_platform != "Home Depot"
                    or product.title != row.get("search_results.product.title")
                    or product.link != row.get("search_results.product.link")
                    or product.primary_image
                    != row.get("search_results.product.primary_image")
                    or (
                        product.rating != Decimal(row["search_results.product.rating"])
                        if row.get("search_results.product.rating")
                        else product.rating is not None
                    )
                    or (
                        product.ratings_total
                        != int(row["search_results.product.ratings_total"])
                        if row.get("search_results.product.ratings_total")
                        else product.ratings_total is not None
                    )
                    or (
                        product.price
                        != Decimal(row["search_results.offers.primary.price"])
                        if row.get("search_results.offers.primary.price")
                        else product.price is not None
                    )
                    or product.currency
                    != row.get("search_results.offers.primary.currency")
                )
                if changed:
                    product.search_term = search_term_lc
                    product.source_platform = "Home Depot"
                    product.title = row.get("search_results.product.title")
                    product.link = row.get("search_results.product.link")
                    product.primary_image = row.get(
                        "search_results.product.primary_image"
                    )
                    product.rating = (
                        Decimal(row["search_results.product.rating"])
                        if row.get("search_results.product.rating")
                        else None
                    )
                    product.ratings_total = (
                        int(row["search_results.product.ratings_total"])
                        if row.get("search_results.product.ratings_total")
                        else None
                    )
                    product.price = (
                        Decimal(row["search_results.offers.primary.price"])
                        if row.get("search_results.offers.primary.price")
                        else None
                    )
                    product.currency = row.get("search_results.offers.primary.currency")
                    product.updated_by = user
                    product.updated_at = timezone.now()
                    product.save()
                    products.append(product)
                # else: no change, do nothing
            except Product.DoesNotExist:
                # Insert new product
                product = Product(
                    search_term=search_term_lc,
                    source_platform="Home Depot",
                    title=row.get("search_results.product.title"),
                    item_id=item_id,
                    link=row.get("search_results.product.link"),
                    primary_image=row.get("search_results.product.primary_image"),
                    rating=(
                        Decimal(row["search_results.product.rating"])
                        if row.get("search_results.product.rating")
                        else None
                    ),
                    ratings_total=(
                        int(row["search_results.product.ratings_total"])
                        if row.get("search_results.product.ratings_total")
                        else None
                    ),
                    price=(
                        Decimal(row["search_results.offers.primary.price"])
                        if row.get("search_results.offers.primary.price")
                        else None
                    ),
                    currency=row.get("search_results.offers.primary.currency"),
                    created_by=user,
                    updated_by=user,
                )
                product.save()
                products.append(product)

        return products, None
    except Exception as e:
        return None, f"Error searching products: {str(e)}"
