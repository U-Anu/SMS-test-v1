from django import template

register = template.Library()


def check_string(value):
    sub_value = '.None'
    if sub_value in value:
        return True
    else:
        return False


@register.filter
def get_field_value(obj, field_name):
    value = getattr(obj, field_name, '')
    value = str(value)
    resp = check_string(value)
    if resp:
        pass
    else:
        return value
@register.filter
def convert_positive(value):
    return value*-1