import os
import typing
import datetime
from datetime import timedelta
from model_utils import Choices

from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage

from .utils import CoreModel
from notification.models import Notification, NotificationVerb, NotificationSetting
from notification import NotifyMixin

if typing.TYPE_CHECKING:
    User = settings.AUTH_USER_MODEL


def get_file_name(instance, filename):
    """
    Return the path of the final path of the document on the filsystem.
    """
    now = timezone.now().strftime("%Y/%m/%d")
    return (
        f"documents/{instance.content_type.name}/{now}/{instance.object_id}_{filename}"
    )


class Document(CoreModel, NotifyMixin):
    """
    Represents a document
    """

    type = Choices(
        ("not_specified", "Not Specified"),
        ("agreement", "Agreement"),
        ("ethics_approval", "Ethics Approval"),
        ("consent_form", "Consent Form"),
        ("subject_information_sheet", "Subject Information Sheet"),
        ("project_proposal", "Project Proposal"),
        ("data_protection_impact_assessment", "Data Protection Impact Assessment"),
        ("other", "Other"),
    )

    class Meta:
        app_label = "core"
        get_latest_by = "added"
        ordering = ["added"]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    content = models.FileField(upload_to=get_file_name, blank=False)
    content_url = models.URLField(verbose_name="Document Url", null=True, blank=True)
    content_notes = models.TextField(
        verbose_name="Document Notes", blank=True, null=True
    )
    domain_type = models.TextField(
        verbose_name="Domain Type", choices=type, default=type.not_specified
    )

    expiry_date = models.DateField(
        verbose_name="Expiry date",
        blank=True,
        help_text="If the document has a validity period, please specify the expiry date here.",
        null=True,
    )

    def __str__(self):
        return f"{self.content.name} ({self.content_object})"

    @property
    def shortname(self):
        """
        Return the name of the files without the path relative to MEDIA_ROOT.
        Also remove the id prefix of the document.
        """
        return "".join(os.path.basename(self.content.path).split("_")[1:])

    @property
    def size(self):
        return self.content.size

    @staticmethod
    def get_notification_recipients():
        """
        Get distinct users that are local custodian of a dataset.
        """

        return (
            get_user_model()
            .objects.filter(Q(project_set__isnull=False) | Q(contracts__isnull=False))
            .distinct()
        )

    @classmethod
    def make_notifications(cls, exec_date: datetime.date):
        recipients = cls.get_notification_recipients()
        for user in recipients:
            notification_setting: NotificationSetting = (
                Document.get_notification_setting(user)
            )
            if not (
                notification_setting.send_email or notification_setting.send_in_app
            ):
                continue
            day_offset = timedelta(days=notification_setting.notification_offset)

            docs = set()
            _ = [docs.update(p.legal_documents.all()) for p in user.project_set.all()]
            _ = [docs.update(c.legal_documents.all()) for c in user.contracts.all()]

            for doc in docs:
                if doc.expiry_date and doc.expiry_date - day_offset == exec_date:
                    cls.notify(user, doc, NotificationVerb.expire)

    @staticmethod
    def notify(user: "User", obj: "Document", verb: "NotificationVerb"):
        """
        Notifies concerning users about the entity.
        """
        offset = user.notification_setting.notification_offset
        dispatch_by_email = user.notification_setting.send_email
        dispatch_in_app = user.notification_setting.send_in_app

        msg = f"The Document {obj.shortname} is expiring in {offset} days."
        on = obj.expiry_date

        Notification.objects.create(
            recipient=user,
            verb=verb,
            message=msg,
            on=on,
            dispatch_by_email=dispatch_by_email,
            dispatch_in_app=dispatch_in_app,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
        ).save()


@receiver(post_delete, sender=Document, dispatch_uid="document_delete")
def document_cleanup(sender, instance, **kwargs):
    if hasattr(instance.content, "path") and os.path.exists(instance.content.path):
        default_storage.delete(instance.content.path)
