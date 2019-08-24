import re
from django import template
from django.template.defaultfilters import stringfilter

tex_re = re.compile(r'([&$#{}%]{1})')
register = template.Library()


@register.filter
@stringfilter
def texify(value):
    """ Escape symbols that have meaning to TeX. """
    return tex_re.sub(r'\\\1', value)
