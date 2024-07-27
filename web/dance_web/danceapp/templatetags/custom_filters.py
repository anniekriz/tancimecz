from django import template
from django.utils import timezone

register = template.Library()

DAYS_SHORT = ['po', 'út', 'st', 'čt', 'pá', 'so', 'ne']

@register.filter
def filter_past_events(events):
    now = timezone.now()
    future_events = []
    for event in events:
        if hasattr(event, 'end'):
            if isinstance(event.end, timezone.datetime):
                if timezone.localtime(event.end) >= now:
                    future_events.append(event)
            else:
                if event.end >= now.date():
                    future_events.append(event)
        elif hasattr(event, 'date'):
            if event.date >= now.date():
                future_events.append(event)
    return future_events

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
        time = f"{format_time(start)}" if isinstance(event, timezone.datetime) else format_time(event.parent.time)
    else:
        if start.month == end.month:
            date = f"{start.day}–{end.strftime('%d.%m.')}".replace('.0', '.')
        else:
            date = f"{start.day}.{start.month}.–{end.day}.{end.month}."
        day = f"{DAYS_SHORT[start.weekday()]}-{DAYS_SHORT[end.weekday()]}"
        time = None

    return {'date': date, 'day': day, 'time': time}
