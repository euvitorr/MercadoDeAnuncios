from datetime import datetime
import logging
import os
import re
from io import BytesIO
from os.path import splitext
from uuid import uuid4

import boto3
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import models
from django.dispatch import receiver
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from embed_video.fields import EmbedVideoField
from PIL import Image

from core.validator import (
    validate_ext_icon,
    validate_ext_image,
    validate_ext_pdf,
    validate_ext_video,
)
from users.forms import User

logger = logging.getLogger(__name__)


def logo_upload_to(instance, filename):
    _, filename_ext = splitext(filename)
    return f"logo/{instance.pk}/{uuid4()}.{filename_ext}"


# User = get_user_model()
def product_upload_to(instance, filename):
    _, filename_ext = splitext(filename)
    # remove any not number in string
    clean_cnpj = re.sub("\D", "", instance.cnpj)
    return f"{instance.__class__.__name__}/{clean_cnpj}/{uuid4()}{filename_ext}".lower()


def genereic_product_upload_to(instance, filename):
    _, filename_ext = splitext(filename)
    return f"{instance.__class__.__name__}/{instance.product.pk}/{uuid4()}{filename_ext}".lower()


def genereic_project_upload_to(instance, filename):
    _, filename_ext = splitext(filename)
    return f"{instance.__class__.__name__}/{instance.project.pk}/{uuid4()}{filename_ext}".lower()


class Timestamp(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(models.Model):

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sku = models.CharField("SKU", max_length=100)
    name = models.CharField("Nome", max_length=100)
    quantity = models.IntegerField("Quantidade", max_length=100, default=0)
    company = models.ForeignKey("integration.ValidML", default='1', blank=True, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=logo_upload_to, null=True, blank=True, validators=[validate_ext_image]
    )
    def __str__(self):
        return self.name

class ProductLink(models.Model):
    class Meta:
        verbose_name = "Link de Produto Mercado Livre"
        verbose_name_plural = "Links de Produto Mercado Livre"
    link = models.CharField("Link Url", max_length=100, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default='b354fb15-1eb7-43fd-aa47-a3f14c3b0670')
    def __str__(self):
        return self.link


class productImage(Timestamp):
    image = models.FileField(
        "Image",
        upload_to=genereic_product_upload_to,
        validators=[validate_ext_image],
        blank=True,
        null=True,
    )
    title = models.CharField(
        "Titulo", max_length=100, blank=True, null=True, default=""
    )
    summary = models.TextField("Resumo", blank=True, null=True)
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="product_images"
    )

    class Meta:
        verbose_name = "Imagens do Produto"
        verbose_name_plural = "Imagens dos Produtos"

    def __str__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        if self.image:
            buffer = BytesIO()
            THUMBNAIL_SIZE = (300, 300)

            image = Image.open(self.image.file)
            image.convert("RGB")
            image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

            filename, ext = splitext(self.image.name.strip())
            _format = ext.replace(".", "")

            if _format.lower() == "jpg":
                _format = "JPEG"

            image.save(buffer, format=_format)
            file_object = File(buffer)
            file_object.name = filename
            file_object.content_type = f"image/{ext.lower()}"
            self.image.save(f"{filename}.{ext}", file_object, save=False)
        super(productImage, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=productImage)
def product_image_delete_image_when_delete(sender, instance, **kwargs):
    if settings.USE_S3:
        s3 = boto3.client("s3")
        product_image = f"media/{instance.image.name}"
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=product_image)
        logger.info(f"delete file {product_image} on S3")
    else:
        try:
            os.remove(instance.image.path)
        except FileNotFoundError as e:
            logger.error(
                f"error handler {e.__class__.__name__} {str(e)}", exc_info=True
            )


@receiver(models.signals.pre_save, sender=productImage)
def product_image_delete_image_when_change(sender, instance, **kwargs):
    if instance.pk is not None:
        old_product_image = productImage.objects.get(pk=instance.pk).image

        if len(old_product_image.name) > 0 and (
            old_product_image.name != instance.image.name
        ):
            try:
                if not settings.USE_S3:
                    os.remove(old_product_image.path)
                else:
                    s3 = boto3.client("s3")
                    product_image = f"media/{old_product_image.file.name}"
                    s3.delete_object(
                        Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=product_image
                    )
                    logger.info(f"delete file {product_image} on S3")
            except FileNotFoundError as e:
                logger.error(
                    f"error handler {e.__class__.__name__} {str(e)}", exc_info=True
                )


class History(models.Model):
    class Meta:
        verbose_name = "Histórico"
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField("Criado em",auto_now_add=True)
    change = models.CharField("Mudança", max_length=100)
    company = models.ForeignKey("integration.ValidML", default='1',blank=True, on_delete=models.CASCADE)