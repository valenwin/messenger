from django.conf import settings
from django.db import models
from .managers import MessageManager


class Thread(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="user_threads", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Thread"
        verbose_name_plural = "Threads"

    def get_unread_messages(self):
        return Message.objects.filter(is_read=False)


class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="sender_messages",
        null=True,
    )
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="thread_messages"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return (
            f"Message: {self.id}; "
            f"Read: {self.is_read}; "
            f"{self.created_at.strftime('%d, %b %Y - %Hh %Mm')}"
        )
