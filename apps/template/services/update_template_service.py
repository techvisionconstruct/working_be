from typing import Optional, Tuple

from apps.template.models import Template
from apps.user.models import User
from apps.trade.models import Trade
from apps.variable.models import Variable
from helpers.process_base64_image import process_base64_image
from helpers.formula_utils import get_variable_details, update_element_formulas

from helpers.create_derived_variable import create_derived_variable
from helpers.create_derived_trade import create_derived_trade


def update_template_service(
    template_id: str, payload: dict, user: User
) -> Tuple[Optional[Template], Optional[str]]:
    try:
        # Check if the template exists
        try:
            template = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return None, f"Template with ID {template_id} not found."

        # Check permissions
        if template.created_by != user and (
            template.owner != user and user.is_staff is not True
        ):
            return None, "You don't have permission to update this template."

        # Process image if provided
        if "image" in payload:
            image = payload["image"]
            if image:
                try:
                    image_file = process_base64_image(image)
                    template.image = image_file
                except Exception as e:
                    return None, f"Error processing image: {str(e)}"
            else:
                # If empty string or null is provided, clear the image
                template.image = None

        # Update basic fields if provided
        if "name" in payload:
            template.name = payload["name"]

        if "description" in payload:
            template.description = payload["description"]

        if "status" in payload:
            template.status = payload["status"]

        if "is_public" in payload:
            template.is_public = payload["is_public"]

        # Update source_id if provided (only if template is 'derived')
        if "source_id" in payload and template.origin == "derived":
            try:
                source_template = Template.objects.get(id=payload["source_id"])

                # Check if user has access to the source template
                if not source_template.is_public and source_template.created_by != user:
                    return (
                        None,
                        "You don't have permission to use this template as a source.",
                    )

                template.source_id = source_template
            except Template.DoesNotExist:
                return (
                    None,
                    f"Source template with ID {payload['source_id']} not found.",
                )

        # Add trades if provided
        if "trades" in payload:
            derived_trades = []
            for trade_id in payload["trades"]:
                try:
                    source_trade = Trade.objects.get(id=trade_id)
                    # Create a derived trade based on the source trade
                    derived_trade = create_derived_trade(source_trade, user, template)
                    derived_trades.append(derived_trade)
                except Trade.DoesNotExist:
                    return None, f"Trade with ID {trade_id} does not exist."
                except Exception as e:
                    return None, f"Error creating derived trade: {str(e)}"

            # Set the derived trades on the template
            template.trades.set(derived_trades)

        # Add variables if provided
        if "variables" in payload:
            derived_variables = []
            variable_id_mapping = {}

            for variable_id in payload["variables"]:
                try:
                    source_variable = Variable.objects.get(id=variable_id)
                    derived_variable, id_map = create_derived_variable(
                        source_variable, user
                    )
                    derived_variables.append(derived_variable)

                    variable_id_mapping.update(id_map)
                except Variable.DoesNotExist:
                    return None, f"Variable with ID {variable_id} does not exist."
                except Exception as e:
                    return None, f"Error creating derived variable: {str(e)}"

            template.variables.set(derived_variables)

            if (
                derived_variables
                and hasattr(template, "trades")
                and template.trades.exists()
            ):

                for trade in template.trades.all():
                    for element in trade.elements.all():
                        formula_updated = False

                        formula_updated = update_element_formulas(
                            element, variable_id_mapping
                        )

                        if formula_updated:
                            element.save()

        template.owner = user

        # Update audit information
        template.updated_by = user

        # Save changes
        template.save()

        return template, None
    except Exception as e:
        return None, f"Error updating template: {str(e)}"
