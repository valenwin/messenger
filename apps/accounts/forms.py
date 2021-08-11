from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.accounts.models import User

User = get_user_model()


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["email"]

    username_email = forms.CharField(max_length=254)

    class Meta:
        model = User
        fields = ("username_email",)

    def clean_username_email(self):
        username_email = self.cleaned_data.get("username_email")
        try:
            User.objects.get(
                Q(username__iexact=username_email) | Q(email__iexact=username_email)
            )
        except get_user_model().DoesNotExist:
            raise ValidationError(
                "The username/email you entered is not registered. "
                "Please enter valid username/email."
            )
        return username_email

    def get_users(self, username_email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = get_user_model()._default_manager.filter(
            Q(username__iexact=username_email) | Q(email__iexact=username_email),
            is_active=True,
        )
        return (u for u in active_users if u.has_usable_password())

    def save(
            self,
            domain_override=None,
            subject_template_name="registration/password_reset_subject.txt",
            email_template_name="registration/password_reset_email.html",
            use_https=False,
            token_generator=default_token_generator,
            from_email=None,
            request=None,
            html_email_template_name=None,
            extra_email_context=None,
    ):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        username_email = self.cleaned_data["username_email"]
        for user in self.get_users(username_email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                "email": user.email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
            }

            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user.email,
                html_email_template_name=html_email_template_name,
            )


class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]
