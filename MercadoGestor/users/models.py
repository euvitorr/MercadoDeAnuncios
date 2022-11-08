import logging
import os
from os.path import splitext
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

logger = logging.Logger(__name__)


def avatar_upload_to(instance, filename):
    _, filename_ext = splitext(filename)
    return f"avatars/{instance.pk}/{uuid4()}.{filename_ext}"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """ create aregular user """
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """ create super user """
        extra_fields.setdefault("is_allowed", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, is_admin=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model  """
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to=avatar_upload_to, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    cpf = models.CharField("CPF", max_length=20, blank=True, null=True)
    company = models.CharField("Empresa", max_length=20, blank=True, null=True)
    birth = models.DateField(null=True ,blank=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    is_allowed = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    @property
    def get_absolute_avatar_url(self):
        return f"{settings.STATIC_URL}{self.avatar.url}"

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(
        self, subject, message, from_email=settings.DEFAULT_FROM_MAIL, **kwargs
    ):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Address(models.Model):
    owner = models.OneToOneField("users.User", on_delete=models.CASCADE)
    state = models.CharField("UF", max_length=30)
    street = models.CharField("Rua", max_length=30)
    city = models.CharField("Cidade", max_length=30)
    zipcode = models.CharField("CEP", max_length=30)
    country = models.CharField("Pais", max_length=30)
    neighborhood = models.CharField("Bairro", max_length=30)
    street_number = models.CharField("Numero", max_length=30)
    complement = models.CharField(
        "Complemento", max_length=30, null=True, blank=True, default=""
    )
    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return f"{self.street}, {self.street_number} , {self.zipcode}"

    def get_short_address(self):
        return f"{self.street}, {self.street_number} ,{self.complement} ,{self.zipcode}"

    def get_full_address(self):
        return f"{self.street}, {self.street_number} ,{self.complement} ,{self.zipcode} {self.city}, {self.state} {self.contry}"


@receiver(models.signals.pre_save, sender=User)
def delete_avatar_when_image_change(sender, instance, *args, **kwargs):
    if settings.USE_S3:
        pass
    else:
        if instance.pk is not None:
            old_avatar = User.objects.get(pk=instance.pk).avatar
            if len(old_avatar.name) > 0 and (old_avatar.name != instance.avatar.name):
                try:
                    os.remove(old_avatar.path)
                except FileNotFoundError as e:
                    logger.error(
                        f"error handler {e.__class__.__name__} {str(e)}", exc_info=True
                    )


@receiver(models.signals.post_delete, sender=User)
def delete_avatar_when_user_deleted(sender, instance, *args, **kwargs):
    if settings.USE_S3:
        pass
    else:
        if instance.avatar:
            try:
                os.remove(instance.avatar.path)
            except FileNotFoundError as e:
                logger.error(
                    f"error handler {e.__class__.__name__} {str(e)}", exc_info=True
                )
