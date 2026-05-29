from django import template

register = template.Library()

@register.filter
def short_id(value, prefix="TXN"):
    if not value:
        return ""
    clean = value.split("_")[-1] if "_" in value else value
    short = clean[-8:].upper()
    return f"{prefix}-{short}"

@register.filter
def comma(value):
    try:
        num = int(float(str(value).replace(',', '')))
        if num < 0:
            return '-' + _indian_format(-num)
        return _indian_format(num)
    except (ValueError, TypeError):
        return value or "0"

def _indian_format(n):
    s = str(n)
    if len(s) <= 3:
        return s
    last3 = s[-3:]
    rest = s[:-3]
    groups = []
    while len(rest) > 2:
        groups.append(rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.append(rest)
    groups.reverse()
    return ','.join(groups) + ',' + last3
