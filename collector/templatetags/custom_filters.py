from django import template

register = template.Library()

@register.filter
def contains_non_empty_dicts(value):
    """Check if a list contains any non-empty dictionaries."""
    if isinstance(value, list):
        return any(bool(d) for d in value if isinstance(d, dict))
    return False