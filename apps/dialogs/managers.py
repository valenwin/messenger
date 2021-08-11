from django.db import models


class MessageManager(models.Manager):
    """
    Returns QuerySet for Message model with filters for is_read field
    Message.objects.read()
    Message.objects.unread()
    """

    def read(self):
        return super().filter(is_read=True)

    def unread(self):
        return super().filter(is_read=False)
