from django import template

register = template.Library()

@register.filter
def dictkey(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return None
