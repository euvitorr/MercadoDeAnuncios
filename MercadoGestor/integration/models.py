import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models



class ValidML(models.Model):

    class Meta:
        verbose_name = "Integração do Mercado Livre"
        verbose_name_plural = "Integrações do Mercado Livre"


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField("Codigo", max_length=100)
    company = models.CharField("Empresa", max_length=100)
    access_token = models.CharField("Token de Acesso", max_length=100)
    client_id = models.CharField("Id Cliente", max_length=100)
    client_secret = models.CharField("Segredo do Cliente", max_length=100)
    create_at = models.DateTimeField("Realizado em", auto_now_add=True)
    expires_in = models.DateTimeField("Expiração de Token")

