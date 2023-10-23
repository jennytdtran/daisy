from django.urls import path
from notification.views import (
    NotificationAdminView,
    NotificationsListView,
    NotificationSettingEditView,
)
from notification.api import dismiss_notification

notif_urls = [
    # Notifications
    path(
        "",
        NotificationsListView.as_view(),
        name="notifications",
    ),
    path(
        "admin",
        NotificationAdminView.as_view(),
        name="notifications_admin",
    ),
    path(
        "admin/<int:pk>",
        NotificationAdminView.as_view(),
        name="notifications_admin_for_user",
    ),
    path(
        "settings",
        NotificationSettingEditView.as_view(),
        name="notifications_settings",
    ),
    # API
    path("/api/dismiss/<int:pk>", dismiss_notification, name="dismiss"),
]