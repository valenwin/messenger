from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView

from apps.accounts.forms import CustomPasswordResetForm, CustomUserRegisterForm
from apps.accounts.models import User


class CustomUserLoginView(LoginView):
    template_name = "login/login.html"


class CustomUserLoginSuccessView(TemplateView):
    template_name = "login/login_success.html"


class CustomUserLogoutView(LogoutView):
    template_name = "login/logout.html"


class CustomUserResetPasswordView(PasswordResetView):
    template_name = "reset_pass/password_reset.html"
    email_template_name = "reset_pass/password_reset_email.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomUserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "reset_pass/password_reset_done.html"


class CustomUserResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = "reset_pass/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class CustomUserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "reset_pass/password_reset_complete.html"


class CustomUserProfile(DetailView):
    model = User
    template_name = "login/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        context["user"] = user
        return context


class CustomUserSignUpView(SuccessMessageMixin, CreateView):
    template_name = "signup.html"
    success_url = reverse_lazy("accounts:sign_in")
    form_class = CustomUserRegisterForm
    success_message = "Your profile was created successfully"
