from django.template import Library

register = Library()


@register.filter(name="format_cnpj")
def format_cnpj(cnpj):
    return "{0}.{1}.{2}/{3}-{4}".format(
        cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:]
    )
