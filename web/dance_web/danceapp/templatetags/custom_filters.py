from django import template
from django.utils import timezone
from danceapp.models import Event, Workshop

register = template.Library()

DAYS_SHORT = ['po', 'út', 'st', 'čt', 'pá', 'so', 'ne']

@register.filter
def filter_past_events(events):
    now = timezone.now()
    future_events = []
    for event in events:
        if hasattr(event, 'end'):
            if isinstance(event.end, timezone.datetime):
                if event.end >= now:
                    future_events.append(event)
            else:
                if event.end >= now.date():
                    future_events.append(event)
        elif hasattr(event, 'date'):
            if event.date >= now.date():
                future_events.append(event)
        elif hasattr(event, 'start'):
            if event.start >= now.date():
                future_events.append(event)
    return future_events

@register.filter
def show_past_events(events):
    if events is None:
        return []
    now = timezone.now()
    past_events = []
    for event in events:
        if hasattr(event, 'end'):
            if isinstance(event.end, timezone.datetime):
                if event.end < now:
                    past_events.append(event)
            else:
                if event.end < now.date():
                    past_events.append(event)
        elif hasattr(event, 'date'):
            if event.date < now.date():
                past_events.append(event)
        elif hasattr(event, 'start'):
            if event.start < now.date():
                past_events.append(event)
    return past_events

@register.filter
def date_format(event):
    if hasattr(event, 'start') and hasattr(event, 'end'):
        start = timezone.localtime(event.start) if isinstance(event.start, timezone.datetime) else event.start
        end = timezone.localtime(event.end) if isinstance(event.end, timezone.datetime) else event.end
    else:
        start = event.date
        end = event.date

    def format_time(t):
        return t.strftime('%H:%M').lstrip('0').replace(' 0', ' ')

    def format_date(d):
        return f"{d.day}.{d.month}."

    if start == end:
        date = format_date(start)
        day = f"{DAYS_SHORT[start.weekday()]}"
        if isinstance(event, Event):
            startTime = format_time(event.parent.startTime)
            endTime = format_time(event.parent.endTime) if event.parent.endTime else None
        else:
            startTime = None
            endTime = None
    else:
        if start.month == end.month:
            date = f"{start.day}.–{end.day}.{end.month}."
        else:
            date = f"{start.day}.{start.month}.–{end.day}.{end.month}."
        day = f"{DAYS_SHORT[start.weekday()]}-{DAYS_SHORT[end.weekday()]}"
        startTime = None
        endTime = None

    return {
        'date': date,
        'day': day,
        'startTime': startTime,
        'endTime': endTime
    }


@register.filter
def is_instance(obj, class_name):
    return obj.__class__.__name__ == class_name

@register.filter
def flag_emoji(iso_code: str) -> str:
    """
    Convert ISO 3166-1 alpha-2 (e.g. 'SK') to flag emoji.
    Returns '' if CZ or invalid.
    """
    if not iso_code or len(iso_code) != 2 or iso_code.upper() == 'CZ':
        return ''
    return ''.join(chr(0x1F1E6 + ord(c.upper()) - ord('A')) for c in iso_code)
