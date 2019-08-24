from django.core import mail
from django.test import TestCase


class SendResoTests(TestCase):
    def setUp(self):
        pass

    def test_basic_send_mail(self):
        mail.send_mail("Subject", "Message", "from@test.com", ["to@test.com"], fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
