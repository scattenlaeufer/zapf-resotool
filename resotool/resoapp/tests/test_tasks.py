from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings
import imaplib
import pathlib
import ssl
import time
import toml
from unittest import skip, skipUnless

from resoapp.models import Recipient, Resolution, ResolutionEmail, SendStatus
from resoapp.tasks import send_reso
from utils import celery_is_up


test_config_path = pathlib.Path(__file__).parent / "celery_mail_test_settings.toml"
if test_config_path.exists():
    test_config = toml.loads(test_config_path.read_text())
else:
    test_config = None


class BasicMailTests(TestCase):
    def setUp(self):
        self.reso = Resolution(title="Test Reso", reso_text="Lorem Ipsum")
        self.reso.save()
        self.mail_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.sender = "Test Out <test-out@test.com>"
        self.subject = "Test Reso Mail"


class SendMailTests(BasicMailTests):
    def setUp(self):
        super().setUp()
        self.reso.recipient_set.create(name="Test Recipient 1", email="test1@test.com")
        self.reso.recipient_set.create(name="Test Recipient 2", email="test2@test.com")

    def test_basic_mail_sending(self):
        result = send_reso(self.reso.pk, self.mail_text, self.subject, self.sender)
        self.assertEqual(result, len(mail.outbox))
        self.assertEqual(len(self.reso.recipient_set.all()), len(mail.outbox))
        self.assertEqual(
            len(self.reso.recipient_set.all()), len(ResolutionEmail.objects.all())
        )


@skipUnless(celery_is_up(), "No Celery instance found!")
@skipUnless(test_config_path.exists(), "No settings for celery mail tests found!")
@override_settings(
    EMAIL_BACKEND="djcelery_email.backends.CeleryEmailBackend",
    EMAIL_HOST=test_config["out"]["server"] if test_config else None,
    EMAIL_PORT=test_config["out"]["port"] if test_config else None,
    EMAIL_HOST_USER=test_config["out"]["account"] if test_config else None,
    EMAIL_HOST_PASSWORD=test_config["out"]["password"] if test_config else None,
)
class SendCeleryMailTests(BasicMailTests):
    def setUp(self):
        super().setUp()
        self.sender = f"Test Out <{test_config['out']['email']}>"
        for i, email in enumerate(test_config["in"]["email"]):
            self.reso.recipient_set.create(name=f"Test Recipient {i+1}", email=email)

        ssl_context = ssl.SSLContext()
        self.mail_box = imaplib.IMAP4(
            test_config["in"]["server"], test_config["in"]["port"]
        )
        self.mail_box.starttls(ssl_context)
        self.mail_box.login(test_config["in"]["account"], test_config["in"]["password"])
        self.mail_box.select()
        self.delete_mails()

    def tearDown(self):
        self.delete_mails()
        self.mail_box.close()
        self.mail_box.logout()

    def delete_mails(self):
        response, mail_data = self.mail_box.search(None, "ALL")
        for num in mail_data[0].split():
            self.mail_box.store(num, "+FLAGS", "\\Deleted")
        self.mail_box.expunge()

    def test_basic_mail_sending(self):
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
        response, mail_data = self.mail_box.search(None, "ALL")
        mail_nums = mail_data[0].split()
        self.assertEqual(len(self.reso.recipient_set.all()), len(mail_nums))
