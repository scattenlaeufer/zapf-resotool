from django.core import mail
from django.test import TestCase
from django.urls import reverse

from resoapp import models, views


class ResolutionDetailViewTests(TestCase):
    def setUp(self):
        self.reso = models.Resolution(
            title="Test Reso", reso_text="This is a test reso"
        )
        self.reso.save()

    def test_view_returns_404(self):
        response = self.client.get(
            reverse("resoapp:resolution", args=(self.reso.pk + 1,))
        )
        self.assertEqual(404, response.status_code)

    def test_view_exists(self):
        response = self.client.get(reverse("resoapp:resolution", args=(self.reso.pk,)))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.reso.title)


class SendResoTests(TestCase):
    def setUp(self):
        pass

    def test_basic_send_mail(self):
        mail.send_mail(
            "Subject", "Message", "from@test.com", ["to@test.com"], fail_silently=False
        )
        self.assertEqual(len(mail.outbox), 1)


class BasicResolutionEmailViewTests(TestCase):
    def setUp(self):
        self.reso = models.Resolution(
            title="Test Reso", reso_text="This is a test reso"
        )
        self.reso.save()
        self.recipient = self.reso.recipient_set.create(
            name="Test Name", email="test email", postal_address="Test address"
        )
        self.email = self.reso.resolutionemail_set.create(
            recipient=self.recipient, email_text="Test Email text"
        )


class ResolutionEmailViewTests(BasicResolutionEmailViewTests):
    def test_view_returns_404(self):
        response = self.client.get(
            reverse("resoapp:emaildetail", args=(self.email.pk + 1,))
        )
        self.assertEqual(404, response.status_code)

    def test_view_exists(self):
        response = self.client.get(reverse("resoapp:emaildetail", args=(self.reso.pk,)))
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.email, response.context["object"])
        self.assertTemplateUsed(response, "resoapp/resolutionemail_detail.html")
