from django.urls import path

from apps.dialogs.api import views

app_name = "threads"

urlpatterns = [
    path("threads/", views.ThreadView.as_view(), name="threads_list"),
    path("threads/<pk>/", views.ThreadDetailView.as_view(), name="thread_details"),
    path("threads/<pk>/messages/", views.MessagesView.as_view(), name="messages_list"),
    path(
        "threads/<pk>/messages/read/",
        views.MessageReadView.as_view(),
        name="message_read",
    ),
    path("messages/<pk>/", views.MessageDetailView.as_view(), name="message_details"),
]
