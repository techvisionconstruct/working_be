from typing import List, Dict, Union, Optional
import re


def map_error_to_fields(
    error: Union[str, List[str]],
    error_mappings: Optional[Dict[str, Union[str, List[str]]]] = None,
    default_field: str = "general",
) -> List[Dict[str, str]]:
    field_errors = []

    # If no mappings provided, return a general error
    if error_mappings is None:
        return [
            {"field": default_field, "message": err}
            for err in ([error] if isinstance(error, str) else error)
        ]

    # Convert single error to list for consistent processing
    errors = [error] if isinstance(error, str) else error

    # Process each error
    for err_msg in errors:
        # Check if the error matches any pattern
        mapped = False

        for pattern, fields in error_mappings.items():
            if re.search(pattern, err_msg, re.IGNORECASE):
                # Handle both single field and multiple fields
                if isinstance(fields, list):
                    for field in fields:
                        field_errors.append({"field": field, "message": err_msg})
                else:
                    field_errors.append({"field": fields, "message": err_msg})

                mapped = True
                break

        # If no mapping found, use default field
        if not mapped and default_field:
            field_errors.append({"field": default_field, "message": err_msg})

    return field_errors
