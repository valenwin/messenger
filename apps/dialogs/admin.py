from django.contrib import admin

from apps.dialogs.models import Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "updated_at")
    raw_id_fields = ("participants",)
    ordering = ("created_at",)
    list_per_page = 20


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "thread", "is_read", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("sender", "thread")
    ordering = ("created_at",)
    list_per_page = 20
