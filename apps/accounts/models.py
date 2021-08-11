from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy

from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    password_expire_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_absolute_url(self):
        return reverse_lazy("accounts:profile", kwargs={"pk": self.pk})

    def __str__(self):
        return self.email
