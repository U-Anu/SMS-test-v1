from django import template

register = template.Library()


@register.filter
def get_matching_record(table2_records, record):
    return table2_records.filter(id=record.id).first()

@register.filter
def running_total(item):
    return sum(int(d) for d in item)

@register.filter(name='split')
def split(value, key):
    value.split("key")
    return value.split(key)


@register.filter
def subtract(value, arg):
    return value - arg