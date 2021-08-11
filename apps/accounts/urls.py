from django.urls import path

import apps.accounts.views as views

urlpatterns = [
    path("sign-in/", views.CustomUserLoginView.as_view(), name="sign_in"),
    path(
        "sign-in/success/",
        views.CustomUserLoginSuccessView.as_view(),
        name="sign_in_success",
    ),
    path("profile/<int:pk>", views.CustomUserProfile.as_view(), name="profile"),
    path("logout/", views.CustomUserLogoutView.as_view(), name="logout"),
    path("sign-up/", views.CustomUserSignUpView.as_view(), name="sign_up"),
    path(
        "password_reset/",
        views.CustomUserResetPasswordView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.CustomUserPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomUserResetPasswordConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.CustomUserPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
