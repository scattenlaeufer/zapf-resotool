from django.db import models
from django_enumfield import enum


class ResoType(enum.Enum):
    RESOLUTION = 1
    POSITIONSPAPIER = 2
    SELBSTVERPFLICHTUNG = 3

    labels = {
        RESOLUTION: "Resolution",
        POSITIONSPAPIER: "Positionspapier",
        SELBSTVERPFLICHTUNG: "Selbstverpflichtung",
    }


class SendStatus(enum.Enum):
    SUCCESS = 1
    FAILURE = 2
    IN_PROGRESS = 3
    NOT_SENT = 4

    _transitions = {
        SUCCESS: (FAILURE, IN_PROGRESS, NOT_SENT),
        FAILURE: (SUCCESS, IN_PROGRESS, NOT_SENT),
        IN_PROGRESS: (SUCCESS, FAILURE, NOT_SENT),
        NOT_SENT: (IN_PROGRESS,),
    }


class Resolution(models.Model):
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
        return ResoType.name(self.reso_type)


class AddresseeCollection(models.Model):
    name = models.CharField(max_length=200)


class Addressee(models.Model):
    name = models.CharField(max_length=200)
    resolutions = models.ManyToManyField(Resolution)
    addressee_collection = models.ManyToManyField(AddresseeCollection)
    note = models.TextField(default="")
    email = models.EmailField(default="")
    opening = models.CharField(max_length=200)
    postal_adress = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class ResolutionEmail(models.Model):
    resolution = models.ForeignKey(Resolution, on_delete=models.CASCADE)
    addressee = models.ForeignKey(Addressee, on_delete=models.CASCADE)
    email_text = models.TextField()
    status = enum.EnumField(SendStatus, default=SendStatus.NOT_SENT)

    def send_status_name(self):
        return SendStatus.name(self.send_status)


class UserGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200, default="")
    user_groups = models.ManyToManyField(UserGroup)
    resolutions = models.ManyToManyField(Resolution)

    def __str__(self):
        if self.university:
            return f"{self.name} ({self.university})"
        else:
            return self.name
