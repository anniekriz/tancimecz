from django import template

register = template.Library()

@register.filter
def filter_by_type(events, event_type):
    return [event for event in events if event.type == event_type]
