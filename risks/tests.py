import json
from django.test import TestCase, Client
from .models import Risk, RiskTextField, RiskEnumField, RiskDateTimeField, RiskNumberField

class TestEndPointStatusCodes(TestCase):
    """ Tests the status codes of the endpoint URLs in the Risks app """

    def test_risks(self):
        """ Does /risks/ return status of 200? """
        c = Client()
        response = c.get('/risks/')
        self.assertEqual(response.status_code, 200)

    def test_risk_url(self):
        """ If we add one Risk, does /risks/1/ return a status of 200? """
        risk = Risk.objects.create(name="Boats")
        c = Client()
        response = c.get('/risks/1/')
        self.assertEqual(response.status_code, 200)

    def test_risk_url_404(self):
        """ If we don't add a risk, does /risks/1/ return a status of 404? """
        c = Client()
        response = c.get('/risks/1/')
        self.assertEqual(response.status_code, 404)

class TestEndPointData(TestCase):
    """ Verifies the data returned from the API Endpoints """

    def setUp(self):
        r1 = Risk.objects.create(name='Dinosaurs')
        RiskTextField.objects.create(name='Species', risk=r1)
        RiskDateTimeField.objects.create(name='First found', risk=r1)
        RiskEnumField.objects.create(name='Diet', possible_values='Carnivore|Herbivore|Omnivore', risk=r1)
        RiskNumberField.objects.create(name='Number of legs', risk=r1)

    def test_data_length(self):
        c = Client()
        response = c.get('/risks/1/')
        self.assertEquals(len([response.json()]),1)
