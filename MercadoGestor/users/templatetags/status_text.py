from django.template import Library

register = Library()


@register.filter(name="status_text")
def status_text(status):
    _status = dict(
        paid="text-success",
        completed="text-success",
        refused="text-danger",
        processing="text-warning",
    )
    return _status.get(status)
