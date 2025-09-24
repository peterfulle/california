# Custom template filters for adding CSS classes to form fields

from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    Add a CSS class to a form field widget
    Usage: {{ form.field_name|add_class:"css-class-name" }}
    """
    try:
        if hasattr(field, 'as_widget'):
            # For form fields - render with class
            return field.as_widget(attrs={'class': css_class})
        elif isinstance(field, BoundField):
            # For bound fields - create a copy to avoid modifying the original
            import copy
            field_copy = copy.deepcopy(field)
            if hasattr(field_copy, 'field') and hasattr(field_copy.field, 'widget'):
                existing_classes = field_copy.field.widget.attrs.get('class', '')
                if existing_classes:
                    field_copy.field.widget.attrs['class'] = existing_classes + ' ' + css_class
                else:
                    field_copy.field.widget.attrs['class'] = css_class
                return field_copy
            else:
                return field  # Return original if structure is unexpected
        else:
            # For other types, try to render as widget with class
            if hasattr(field, 'widget'):
                return field.widget.render(field.name, field.value(), attrs={'class': css_class})
            else:
                return field  # Return original if can't process
    except (AttributeError, TypeError):
        # If anything goes wrong, return the original field
        return field
