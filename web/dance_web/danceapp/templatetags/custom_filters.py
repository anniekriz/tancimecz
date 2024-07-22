from django import template

register = template.Library()

@register.filter
def filter_by_type(events, event_type):
    return [event for event in events if event.type == event_type]

DAYS_SHORT = ['po', 'út', 'st', 'čt', 'pá', 'so', 'ne']

@register.filter
def date_format(event):
    start = event.start
    end = event.end

    # zajistí, že místo 07:00 bude 7:00
    def format_time(t):
        return t.strftime('%H:%M').lstrip('0').replace(' 0', ' ')

    if start.date() == end.date():
        # %H: Hodina ve 24hodinovém formátu (00 až 23), %M: Minuta (00 až 59)
        date = f"{start.strftime('%d.%m. %Y')}"
        day = f"{DAYS_SHORT[start.weekday()]}"
        time = f"{format_time(start)}-{format_time(end)}"
    else:
        date = f"{start.strftime('%d.%m.')}–{end.strftime('%d.%m. %Y')}"
        day = f"{DAYS_SHORT[start.weekday()]}-{DAYS_SHORT[end.weekday()]}"
        time = None

    return {'date': date, 'day': day, 'time': time}
