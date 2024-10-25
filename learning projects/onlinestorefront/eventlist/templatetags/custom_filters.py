from django import template
import datetime

register = template.Library()

@register.filter
def format_cz_date(value):
    if isinstance(value, datetime.datetime):
        months = [
            'ledna', 'února', 'března', 'dubna', 'května', 'června',
            'července', 'srpna', 'září', 'října', 'listopadu', 'prosince'
        ]
        day = value.day
        month = months[value.month - 1]
        year = value.year
        return f"{day}. {month} {year}"
    return value

@register.filter
def format_cz_time(value):
    if isinstance(value, datetime.datetime):
        return value.strftime('%H:%M')
    return value