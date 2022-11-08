import logging
from datetime import datetime
from io import BytesIO
from os.path import splitext
from random import randint

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.files import File
from django.db import transaction
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import redirect, render, resolve_url
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, View
from PIL import Image
from .forms import AddressForm, AvatarForm, SignUpForm, UserForm
from .models import Address
from .token import account_activation_token

User = get_user_model()
logger = logging.getLogger(__name__)


# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    avatar = AvatarForm()
    template_name = "login.html"
    template_success = "home"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form,"avatar_form": avatar})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # conta desativada no momento do cadastro
            user.save()
            current_site = get_current_site(request)
            subject = "Ative sua conta | ManagerML"
            message = render_to_string(
                "email/account_activation_email.txt",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject, message)
            messages.success(request, "Acesse seu e-mail e confirme seu cadastro.")
            return redirect(self.template_success)

        return render(request, self.template_name, {"form_signup": form})


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, ("Your account have been confirmed."))
            return redirect("home")

        else:
            messages.warning(
                request,
                (
                    "The confirmation link was invalid, possibly because it has already been used."
                ),
            )
            return redirect("home")


class ProfileView(LoginRequiredMixin, View):

    model = User
    form_class = UserForm
    template_name = "perfil.html"

    def get_object(self, *args, **kwargs):
        return self.get_queryset().select_related("address").first()

    def get_queryset(self):
        return self.model.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = {**kwargs}
        context["object"] = self.object

        address = None
        if hasattr(self.object, "address"):
            address = self.object.address

        user_data = {}
        for field in self.object._meta.fields:
            if field.name == "id":
                continue

            user_data[field.name] = getattr(self.object, field.name)
        address_data = {}
        if address:
            for field in address._meta.fields:
                if field.name == "id":
                    continue

                address_data[field.name] = getattr(address, field.name)
        context["user_form"] = self.form_class(data=user_data)
        context["avatar_form"] = AvatarForm()
        if not address:
            context["address_form"] = AddressForm()
            return context

        context["address_form"] = AddressForm(data=address_data)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        address = Address.objects.filter(owner=self.object).first()
        logger.info(
            "update user data in request.POST: %s " % {"data": dict(request.POST)}
        )
        user_form = self.form_class(instance=self.object, data=request.POST)
        address_form = AddressForm(instance=address, data=request.POST)
        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address = address_form.save(commit=False)
            address.owner = self.object
            address.save()
            messages.success(request, "Perfil atualizado com sucesso.")
        else:
            logger.warning(
                "error on update user prfile data: %s"
                % {
                    "data": request.POST,
                    "error_users": user_form.errors,
                    "error_address": address_form.errors,
                }
            )
            messages.error(request, "Erros form encontrados, verifique o formulário")
        context["user_form"] = user_form
        context["address_form"] = address_form
        return render(request, self.template_name, context)


@csrf_exempt
def update_avatar(request, pk):
    context = {}
    logger.info("request send with file, %s" % request.FILES)
    form = AvatarForm(request.POST, request.FILES)
    if form.is_valid():
        x = form.cleaned_data.get("x")
        y = form.cleaned_data.get("y")
        w = form.cleaned_data.get("width")
        h = form.cleaned_data.get("height")
        avatar = form.cleaned_data.get("avatar")

        buffer = BytesIO()
        image = Image.open(avatar.file)
        image.convert("RGB")
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        filename, ext = splitext(avatar.name.strip())
        _format = ext.replace(".", "")

        if _format.lower() == "jpg":
            _format = "JPEG"

        resized_image.save(buffer, format=_format)
        file_object = File(buffer)
        file_object.content_type = "image/jpeg"
        request.user.avatar.save(filename, file_object)
        request.user.save()

        context["success"] = True
        messages.success(request, "Foto foi alterada com sucesso.")
        message = render_to_string("message.html", context=context, request=request)
        context["message"] = message
        context["avatar"] = User.objects.get(pk=request.user.pk).avatar.url
        logger.info("avatar updated %s" % context)
        return JsonResponse(context)

    context["success"] = False
    context["message"] = form.errors
    logger.warning("avatar not updated form is not valid error:%s" % context)
    return JsonResponse(context)
