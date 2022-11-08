from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy

from .forms import LoginForm
from .views import (
    ActivateAccount,
    ProfileView,
    SignUpView,
    update_avatar,
)
from core.views import HomeTemplateView

urlpatterns = [
    # path('login', login,  name='login'),
    # path('logout', logout ,  name='logout'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", ActivateAccount.as_view(), name="activate"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            from_email=settings.DEFAULT_FROM_MAIL,
            email_template_name="email/password_reset_email.txt",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("perfil/upadte_avatar/<int:pk>", update_avatar, name="update_avatar"),
    path("perfil/", HomeTemplateView.as_view(), name="profile"),
]
