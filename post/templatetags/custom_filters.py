# myapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def is_checked(value, tag_id):
    """Check if a tag ID is in the list of filters."""
    return str(tag_id) in value