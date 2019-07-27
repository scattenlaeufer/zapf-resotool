from django.test import TestCase

from resoapp import models


class ResolutionTests(TestCase):

    def test_basic_resolution_generation(self):
        test_reso = models.Resolution(title="Testreso 1", reso_text="lorem ipsum")
        test_reso.save()

        self.assertIn(test_reso, models.Resolution.objects.all())
