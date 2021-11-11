from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

# TODO: Create more robust phone parser (or cave and use another library)
@register.filter
@stringfilter
def format_phone(value):
    return re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', value)