import debug_toolbar
from . import views

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path("", views.home, name="base"),
    path("about-us", views.about_us, name="about_us"),
    path("authors", views.authors, name="authors"),
    path("contacts", views.contacts, name="contacts"),
    path(
        "accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")
    ),
    path("api/v1/auth/", include("apps.accounts.api.urls", namespace="api_auth")),
    path("api/v1/", include("apps.dialogs.api.urls", namespace="api_dialogs")),
]
