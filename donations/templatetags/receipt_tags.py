from django import template

register = template.Library()

@register.filter
def short_id(value, prefix="TXN"):
    if not value:
        return ""
    clean = value.split("_")[-1] if "_" in value else value
    short = clean[-8:].upper()
    return f"{prefix}-{short}"
