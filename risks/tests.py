from django.test import TestCase, Client
from .models import Risk, RiskTextField, RiskEnumField, RiskDateTimeField, RiskNumberField

class TestEndPoints(TestCase):
    """ Tests the endpoint URLs in the Risks app """

    def test_risks(self):
        """ Tests the /risks/ index url """
        c = Client()
        response = c.get('/risks/')
        self.assertEqual(response.status_code, 200)

    def test_risk_url(self):
        """ Tests endpoint of a specific risk """
        risk = Risk.objects.create(name="Boats")
        c = Client()
        response = c.get('/risks/1/')
        self.assertEqual(response.status_code, 200)
