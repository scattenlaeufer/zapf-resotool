"""
Collection of all tests for the views module
"""

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from resotool import models


class ResolutionDetailViewTests(TestCase):
    """
    TestCase for the ResolutionDetailView class
    """

    def setUp(self):
        self.reso = models.Resolution(
            title="Test Reso", reso_text="This is a test reso"
        )
        self.reso.save()

    def test_view_returns_404(self):
        """
        Test to make sure a request of a non existing Resolution object returns
        a 404 error page.
        """

        response = self.client.get(reverse("resolution", args=(self.reso.pk + 1,)))
        self.assertEqual(404, response.status_code)

    def test_view_exists(self):
        """
        Test to make sure a request of an existing Resolution objects returns
        a 200 status and the correct resolution.
        """

        response = self.client.get(reverse("resolution", args=(self.reso.pk,)))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.reso.title)


class SendResoTests(TestCase):
    """
    TestCase for sending resolutions via email
    """

    def setUp(self):
        pass

    def test_basic_send_mail(self):
        """
        Test for basic sending of emails using the locmem email back end
        """
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
        response = self.client.get(reverse("emaildetail", args=(self.email.pk + 1,)))
        self.assertEqual(404, response.status_code)

    def test_view_exists(self):
        response = self.client.get(reverse("emaildetail", args=(self.reso.pk,)))
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.email, response.context["object"])
        self.assertTemplateUsed(response, "resotool/resolutionemail_detail.html")
