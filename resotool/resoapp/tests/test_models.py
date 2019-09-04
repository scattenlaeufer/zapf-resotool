from django.test import TestCase

from resoapp import models


class ResolutionTests(TestCase):
    def test_basic_resolution_generation(self):
        test_reso = models.Resolution(title="Testreso 1", reso_text="lorem ipsum")
        test_reso.save()

        self.assertIn(test_reso, models.Resolution.objects.all())


class ResulutionEmailTests(TestCase):
    def setUp(self):
        self.reso = models.Resolution(title="Testreso 1", reso_text="Test text")
        self.reso.save()
        self.recipient = models.Recipient(
            name="Test Recipient", opening="Dear Test Recipient", postal_address="None"
        )
        self.recipient.save()
        self.mail_text = "Blubb"

    def test_email_creation(self):
        test_email = self.reso.resolutionemail_set.create(
            resolution=self.reso, recipient=self.recipient, email_text=self.mail_text
        )
        self.assertIn(test_email, models.ResolutionEmail.objects.all())
        self.assertEqual(self.mail_text, test_email.email_text)
