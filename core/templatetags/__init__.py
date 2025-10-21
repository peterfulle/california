# Custom template filters for adding CSS classes to form fields

from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    """
    Add a CSS class to a form field widget
    Usage: {{ form.field_name|add_class:"css-class-name" }}
    """
    if hasattr(field, 'as_widget'):
        # For form fields
        return field.as_widget(attrs={'class': css_class})
    else:
        # For bound fields
        existing_classes = field.field.widget.attrs.get('class', '')
        if existing_classes:
            field.field.widget.attrs['class'] = existing_classes + ' ' + css_class
        else:
            field.field.widget.attrs['class'] = css_class
        return field
