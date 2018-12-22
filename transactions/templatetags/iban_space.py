from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def iban_space(value):
    """Add spaces for better reading"""

    control_number = value[:2]

    account = ' '.join([value[i:i+4] for i in range(2, len(value), 4)])

    return "{} {}".format(control_number, account)
