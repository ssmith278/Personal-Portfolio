from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

# TODO: Create more robust phone parser (or cave and use another library)
@register.filter
@stringfilter
def split_string(value, arg='\n'):
    return value.split(arg)