"""
Collection of all database models used by resoapp
"""

from django.db import models
from django_enumfield import enum


class ResoType(enum.Enum):  # pylint: disable=no-init
    """
    A enum to represent all possible resolution types.
    """

    RESOLUTION = 1
    POSITIONSPAPIER = 2
    SELBSTVERPFLICHTUNG = 3

    labels = {
        RESOLUTION: "Resolution",
        POSITIONSPAPIER: "Positionspapier",
        SELBSTVERPFLICHTUNG: "Selbstverpflichtung",
    }


class SendStatus(enum.Enum):  # pylint: disable=no-init
    """
    A enum to reperesnt all possible sent statuses of emails.
    """

    SUCCESS = 1
    FAILURE = 2
    IN_PROGRESS = 3
    NOT_SENT = 4

    labels = {
        SUCCESS: "versandt",
        FAILURE: "fehlgeschlagen",
        IN_PROGRESS: "in Arbeit",
        NOT_SENT: "(noch) nicht versandt",
    }

    _transitions = {
        SUCCESS: (FAILURE, IN_PROGRESS, NOT_SENT),
        FAILURE: (SUCCESS, IN_PROGRESS, NOT_SENT),
        IN_PROGRESS: (SUCCESS, FAILURE, NOT_SENT),
        NOT_SENT: (IN_PROGRESS,),
    }


class Resolution(models.Model):
    """
    Database representation of a resolution
    """

    title = models.CharField(max_length=200)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_enacted = models.DateTimeField(blank=True, null=True)
    date_sent = models.DateField(blank=True, null=True)
    reso_type = enum.EnumField(ResoType, default=ResoType.RESOLUTION)
    reso_text = models.TextField()
    reso_text_html = models.TextField(default="")
    motivation_text = models.TextField(default="")
    motivation_text_html = models.TextField(default="")
    pdf_path = models.FilePathField(default="")

    def __str__(self):
        return self.title

    def reso_type_name(self):
        """
        Return the ResoType label corresponding to the set resolution type

        :return: ResoType label
        :rtype: str
        """
        return ResoType.name(self.reso_type)


class RecipientCollection(models.Model):
    """
    Database representation of a list of recipients

    This will probably not be used in the future and should be considered
    deprecated!
    """

    name = models.CharField(max_length=200)


class Recipient(models.Model):
    """
    Database representation of a recipient of resolutions

    A Recipient object gets created once for every potential recipient of
    resolutions and can get multiple resolutions sent.
    """

    name = models.CharField(max_length=200)
    resolutions = models.ManyToManyField(Resolution)
    recipient_collection = models.ManyToManyField(RecipientCollection)
    note = models.TextField(default="")
    email = models.EmailField(default="")
    opening = models.CharField(max_length=200)
    postal_address = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class ResolutionEmail(models.Model):
    """
    Database representation of a email dispatch a resolution

    A ResolutionEmail object gets created for each Resolution and each
    Recipient, that Resolution should be sent to.
    """

    resolution = models.ForeignKey(Resolution, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    email_text = models.TextField()
    status = enum.EnumField(SendStatus, default=SendStatus.NOT_SENT)

    def send_status_name(self):
        """
        Return the SendStatus label corresponding to the set send status

        :return: SendStatus label
        :rtype: str
        """

        return SendStatus.name(self.status)


class UserGroup(models.Model):
    """
    User group setting to manage rights in the resotool
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(models.Model):
    """
    Database representation of a user of the resotool
    """

    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200, default="")
    user_groups = models.ManyToManyField(UserGroup)
    resolutions = models.ManyToManyField(Resolution)

    def __str__(self):
        if self.university:
            return f"{self.name} ({self.university})"
        else:
            return self.name
