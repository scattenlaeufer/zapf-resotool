"""
Collection of test for all resotapp database models
"""

from django.test import TestCase

from resotool import models


class ResolutionTests(TestCase):
    """
    TestCase for the Resolution model
    """

    def test_basic_resolution_generation(self):
        """
        Test the creation of Resolution objects
        """

        test_reso = models.Resolution(title="Testreso 1", reso_text="lorem ipsum")
        test_reso.save()

        self.assertIn(test_reso, models.Resolution.objects.all())


class ResulutionEmailTests(TestCase):
    """
    TestCase for the ResolutionEmail model
    """

    def setUp(self):
        self.reso = models.Resolution(title="Testreso 1", reso_text="Test text")
        self.reso.save()
        self.recipient = models.Recipient(
            name="Test Recipient", opening="Dear Test Recipient", postal_address="None"
        )
        self.recipient.save()
        self.mail_text = "Blubb"

    def test_email_creation(self):
        """
        Test the creation of ResolutionEmail objects
        """

        test_email = self.reso.resolutionemail_set.create(
            resolution=self.reso, recipient=self.recipient, email_text=self.mail_text
        )
        self.assertIn(test_email, models.ResolutionEmail.objects.all())
        self.assertEqual(self.mail_text, test_email.email_text)
