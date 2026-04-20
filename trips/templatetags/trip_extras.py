from django import template

register = template.Library()



@register.filter(name='duration_label')
def duration_label(trip):

    days = trip.duration_days

    if not days:
        return 'Duration unknown'
    if days == 1:
        return 'Day trip'
    if days <= 3:
        return f"{days}-day adventure"
    if days <= 7:
        return f"{days}-day expedition"
    return f"{days}-day epic"