from os.path import splitext

from django.core.exceptions import ValidationError


def _validate_ext(value, *args):
    filename, ext = splitext(value.name.strip())
    if not ext in args:
        raise ValidationError(
            f"Extão {ext} não é valida para Image, por favor os formatos {', '.join(args)}"
        )

    else:
        return value


def validate_ext_image(value):
    _validate_ext(value, ".jpg", ".jpeg", ".png")


def validate_ext_icon(value):
    _validate_ext(value, ".svg")


def validate_ext_video(value):
    _validate_ext(value, ".mp4", ".mpeg")


def validate_ext_pdf(value):
    _validate_ext(value, ".pdf")
