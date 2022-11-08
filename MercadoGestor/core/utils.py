import re


def is_cpf_or_cnpj(valor):
    # Remove caracteres invalidos do valor
    valor = re.findall("\d+", str(valor))
    valor = "".join(valor)
    # Verifica se é um CPF
    if len(valor) == 11:
        return "CPF"

    # Verifica  se é um  CNPJ
    elif len(valor) == 14:
        return "CNPJ"

    else:
        return False


def valid_cpf_cnpj(valor):
    """Verifica se é CPF pi CNPJ"""
    valida = is_cpf_or_cnpj(valor)
    valor = re.findall("\d+", str(valor))
    valor = "".join(valor)
    if valida == "CPF":
        #  Retorna true para cpf válido
        return valid_cpf(valor)

    elif valida == "CNPJ":
        # Retorna true para CNPJ válido
        return valid_cnpj(valor)

    # Não retorna nada
    else:
        return False


def format_cpf_cnpj(valor):
    # O valor formatado
    formatado = False
    # Verifica se é CPF ou CNPJ
    valida = is_cpf_or_cnpj(valor)
    # Valida CPF
    if valida == "CPF":
        if valid_cpf(valor):
            # Formata o CPF  ###.###.###-##
            formatado = "{0}.{1}.{2}-{3}".format(
                valor[:3], valor[3:6], valor[6:9], valor[9:]
            )
    # Valida CNPJ
    elif valida == "CNPJ":
        if valid_cnpj(valor):
            #  Formata o CNPJ  ##.###.###/####-##
            formatado = "{0}.{1}.{2}/{3}-{4}".format(
                valor[:2], valor[2:5], valor[5:8], valor[8:12], valor[12:]
            )
    # Retorna o valor
    return formatado


def valid_cpf(cpf):
    cpf = "".join(re.findall("\d+", str(cpf)))
    if (not cpf) or (len(cpf) < 11):
        return False

    if (
        cpf == "00000000000"
        or cpf == "11111111111"
        or cpf == "22222222222"
        or cpf == "33333333333"
        or cpf == "44444444444"
        or cpf == "55555555555"
        or cpf == "66666666666"
        or cpf == "77777777777"
        or cpf == "88888888888"
        or cpf == "99999999999"
    ):
        return False

    # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam
    inteiros = list(map(int, cpf))
    novo = inteiros[:9]
    while len(novo) < 11:
        r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return cpf

    return False


def valid_cnpj(cnpj):
    cnpj = "".join(re.findall("\d", str(cnpj)))
    if (not cnpj) or (len(cnpj) < 14):
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]
    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)
    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return cnpj

    return False


def format_cnpj(cnpj):
    return "{0}.{1}.{2}/{3}-{4}".format(
        cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:]
    )


def _validate_regex(value, regex):
    if re.search(regex, value):
        return value

    return False


def validate_email(value):
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    return _validate_regex(value, regex)


def validate_contact_phone(value):
    """
    remove o zero se começar com ele se nao retorna o telefone se for invalido retorna false
    exemplo de formatos validos
    (11) 98800-0088
    (11) 2041-0512
    011 20410512
    11993907727
    (11)993907727
    11 993907727
    011 97051-3508
    4231-4522
    1142314522
    01142314522
    1142314522
    11970513508
    970513508
    42314522
    """
    regex = "(\(?\d{2,3}\))?\s?([9])?(\d{4})-?(\d{4})"
    phone_validate = _validate_regex(value, regex)
    if phone_validate:
        phone_validate = "".join(re.findall("\d", value))
        if phone_validate.startswith("0"):
            return phone_validate[1:]

        return phone_validate

    return False


def format_telefone(value):
    if len(value) == 11:
        # valor esperado 11970513508
        return f"({value[:2]}) {value[2:6]}-{value[7:]}"

    elif len(value) == 10:
        # 112041-0512
        return f"({value[:2]}) {value[2:6]}-{value[6:]}"

    elif len(value) == 9:
        # 920410512
        return f"{value[:5]}-{value[5:]}"

    elif len(value) == 8:
        # 920410512
        return f"{value[:4]}-{value[4:]}"
