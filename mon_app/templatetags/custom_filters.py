from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits a string by the given argument (delimiter).
    Usage: {{ value|split:"," }}
    """
    if value:
        return [item.strip() for item in value.split(arg)]
    return []
