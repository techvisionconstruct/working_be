from django.db import transaction
from apps.template.models import Template
from apps.template.choices import TemplateOrigin
from apps.user.models import User
from helpers.create_derived_trade import create_derived_trade
from helpers.create_derived_variable import create_derived_variable
from helpers.formula_utils import update_element_formulas


def create_derived_template(source_template: Template, user: User) -> Template:

    with transaction.atomic():
        # Create a new template with the same data but as derived
        template = Template.objects.create(
            name=source_template.name,
            description=source_template.description,
            status=source_template.status,
            origin=TemplateOrigin.DERIVED,
            source=source_template,
            owner=source_template.owner,
            is_public=source_template.is_public,
            created_by=user,
            updated_by=user,
        )

        # Create derived trades with their elements
        if source_template.trades.exists():
            derived_trades = []
            for source_trade in source_template.trades.all():
                # This will create a derived trade and all its derived elements
                derived_trade = create_derived_trade(source_trade, user, template)
                print(derived_trade)
                derived_trades.append(derived_trade)

            template.trades.set(derived_trades)

        # Create derived variables
        if source_template.variables.exists():
            derived_variables = []
            variable_id_mapping = {}

            for source_variable in source_template.variables.all():

                derived_variable, id_map = create_derived_variable(
                    source_variable, user
                )
                derived_variables.append(derived_variable)

                variable_id_mapping.update(id_map)

            template.variables.set(derived_variables)

            if derived_variables and template.trades.exists():

                for trade in template.trades.all():
                    for element in trade.elements.all():
                        formula_updated = False

                        formula_updated = update_element_formulas(
                            element, variable_id_mapping
                        )

                        # Save element if formulas were updated
                        if formula_updated:
                            element.save()

        return template
