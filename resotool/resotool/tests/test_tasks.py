"""
Collection of tests for the tasks module
"""

import imaplib
import pathlib
import ssl
import time
from unittest import skipUnless
import toml
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings

from resotool.models import Resolution, ResolutionEmail, SendStatus
from resotool.tasks import send_reso
from utils import celery_is_up


TEST_CONFIG_PATH = pathlib.Path(__file__).parent / "celery_mail_test_settings.toml"
if TEST_CONFIG_PATH.exists():
    TEST_CONFIG = toml.loads(TEST_CONFIG_PATH.read_text())
else:
    TEST_CONFIG = None


class BasicMailTests(TestCase):
    """
    Base class for email sending test cases
    """

    def setUp(self):
        self.reso = Resolution(title="Test Reso", reso_text="Lorem Ipsum")
        self.reso.save()
        self.mail_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.sender = "Test Out <test-out@test.com>"
        self.subject = "Test Reso Mail"


class SendMailTests(BasicMailTests):
    """
    TestCase for sending resolution emails through Django's locmem back end
    """

    def setUp(self):
        super().setUp()
        self.reso.recipient_set.create(name="Test Recipient 1", email="test1@test.com")
        self.reso.recipient_set.create(name="Test Recipient 2", email="test2@test.com")

    def test_basic_mail_sending(self):
        """
        Test sending resolution emails through Django's locmem back end
        """

        result = send_reso(self.reso.pk, self.mail_text, self.subject, self.sender)
        self.assertEqual(result, len(mail.outbox))
        self.assertEqual(len(self.reso.recipient_set.all()), len(mail.outbox))
        self.assertEqual(
            len(self.reso.recipient_set.all()), len(ResolutionEmail.objects.all())
        )


@skipUnless(celery_is_up(), "No Celery instance found!")
@skipUnless(TEST_CONFIG_PATH.exists(), "No settings for celery mail tests found!")
@override_settings(
    EMAIL_BACKEND="djcelery_email.backends.CeleryEmailBackend",
    EMAIL_HOST=TEST_CONFIG["out"]["server"] if TEST_CONFIG else None,
    EMAIL_PORT=TEST_CONFIG["out"]["port"] if TEST_CONFIG else None,
    EMAIL_HOST_USER=TEST_CONFIG["out"]["account"] if TEST_CONFIG else None,
    EMAIL_HOST_PASSWORD=TEST_CONFIG["out"]["password"] if TEST_CONFIG else None,
)
class SendCeleryMailTests(BasicMailTests):
    """
    TestCase for sending resolution emails through the Celery email back end
    """

    def setUp(self):
        super().setUp()
        self.sender = f"Test Out <{TEST_CONFIG['out']['email']}>"
        for i, email in enumerate(TEST_CONFIG["in"]["email"]):
            self.reso.recipient_set.create(name=f"Test Recipient {i+1}", email=email)

        ssl_context = ssl.SSLContext()
        self.mail_box = imaplib.IMAP4(
            TEST_CONFIG["in"]["server"], TEST_CONFIG["in"]["port"]
        )
        self.mail_box.starttls(ssl_context)
        self.mail_box.login(TEST_CONFIG["in"]["account"], TEST_CONFIG["in"]["password"])
        self.mail_box.select()
        self.delete_mails()

    def tearDown(self):
        self.delete_mails()
        self.mail_box.close()
        self.mail_box.logout()

    def delete_mails(self):
        """
        Clear the given test mail box
        """

        _, mail_data = self.mail_box.search(None, "ALL")
        for num in mail_data[0].split():
            self.mail_box.store(num, "+FLAGS", "\\Deleted")
        self.mail_box.expunge()

    def test_basic_mail_sending(self):
        """
        Test sending resolution mails through the Celery email back end
        """

        results = send_reso(self.reso.pk, self.mail_text, self.subject, self.sender)
        for reso_mail in ResolutionEmail.objects.all():
            self.assertEqual(SendStatus.IN_PROGRESS, reso_mail.status)
        self.assertEqual(
            len(self.reso.recipient_set.all()), len(ResolutionEmail.objects.all())
        )
        for result in results:
            self.assertEqual(1, result.get(timeout=5))
        for reso_mail in ResolutionEmail.objects.all():
            self.assertEqual(SendStatus.SUCCESS, reso_mail.status)

        # Give the mails some time to be found in the mail box
        time.sleep(2)

        self.mail_box.select()
        _, mail_data = self.mail_box.search(None, "ALL")
        mail_nums = mail_data[0].split()
        self.assertEqual(len(self.reso.recipient_set.all()), len(mail_nums))
