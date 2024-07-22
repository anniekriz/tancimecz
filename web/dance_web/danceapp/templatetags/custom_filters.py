from django import template
from django.utils import timezone
import datetime

register = template.Library()

@register.filter
def filter_by_type(events, event_type):
    return [event for event in events if event.type == event_type]

DAYS_SHORT = ['po', 'út', 'st', 'čt', 'pá', 'so', 'ne']

@register.filter
def date_format(event):
    start = timezone.localtime(event.start)
    end = timezone.localtime(event.end)

    # zajistí, že místo 07:00 bude 7:00
    def format_time(t):
        return t.strftime('%H:%M').lstrip('0').replace(' 0', ' ')
    
    def format_date(d):
        return f"{d.day}.{d.month}."
    
    if start.date() == end.date():
        date = format_date(start)
        day = f"{DAYS_SHORT[start.weekday()]}"
        time = f"{format_time(start)}-{format_time(end)}"
    else:
        if start.month == end.month:
            date = f"{start.day}–{end.strftime('%d.%m.')}".replace('.0', '.')
        else:
            date = f"{start.day}.{start.month}.–{end.day}.{end.month}."
        day = f"{DAYS_SHORT[start.weekday()]}-{DAYS_SHORT[end.weekday()]}"
        time = None

    return {'date': date, 'day': day, 'time': time}

@register.filter
def filter_past_events(events):
    now = timezone.now()
    return [event for event in events if timezone.localtime(event.end) >= now]
