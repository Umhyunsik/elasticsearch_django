# post_extras.py
from django import template

register = template.Library()
# post_extras.py

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except Exception:
        return ''