from django.db import models

import enum


class ResoType(enum.IntFlag):
    RESOLUTION = enum.auto()
    POSITIONSPAPIER = enum.auto()
    SELBSTVERPFLICHTUNG = enum.auto()


class SendStatus(enum.IntFlag):
    SUCCESS = enum.auto()
    FAILURE = enum.auto()
    IN_PROGRESS = enum.auto()
    NOT_SENT = enum.auto()


class Resolution(models.Model):
    title = models.CharField(max_length=200)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_enacted = models.DateTimeField(blank=True, null=True)
    date_sent = models.DateField(blank=True, null=True)
    reso_type = models.IntegerField(
        default=ResoType.RESOLUTION,
        choices=[(e.value, e.name.lower().replace("_", " ")) for e in ResoType],
    )
    reso_text = models.TextField()
    reso_text_html = models.TextField(default="")
    motivation_text = models.TextField(default="")
    motivation_text_html = models.TextField(default="")
    pdf_path = models.FilePathField(default="")

    def __str__(self):
        return self.title


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
    status = models.IntegerField(
        choices=[(e.value, e.name.lower().replace("_", " ")) for e in SendStatus],
    )


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
