from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("username", "email")
    ordering = ("created_at",)
    list_per_page = 20
