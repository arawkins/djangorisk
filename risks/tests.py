import json
from django.test import TestCase, Client
from .models import Risk, RiskField, RiskTextField, RiskEnumField, RiskDateTimeField, RiskNumberField

class TestEndPointStatusCodes(TestCase):
    """ Tests the status codes of the endpoint URLs in the Risks app """

    def setUp(self):
        self.client = Client()

    def test_risks(self):
        """ Does /risks/ return status of 200? """
        response = self.client.get('/risks/')
        self.assertEqual(response.status_code, 200)

    def test_risk_url(self):
        """ If we add one Risk, does /risks/1/ return a status of 200? """
        risk = Risk.objects.create(name="Boats")
        response = self.client.get('/risks/1/')
        self.assertEqual(response.status_code, 200)

    def test_risk_url_404(self):
        """ If we don't add a risk, does /risks/1/ return a status of 404? """
        response = self.client.get('/risks/1/')
        self.assertEqual(response.status_code, 404)

class TestRisksEndPointData(TestCase):
    """ Tests the data returned from the /risks/ API Endpoint """
    def setUp(self):
        r1 = Risk.objects.create(name='Dinosaurs')
        r2 = Risk.objects.create(name='Planes')
        c = Client()
        self.response = c.get('/risks/').json()

    def test_data_length(self):
        self.assertEquals(len(self.response),2)

class TestRiskIdEndPointData(TestCase):
    """ Tests the data returned from the /risks/<risk:id> API Endpoint """

    def setUp(self):
        # Set up data
        r1 = Risk.objects.create(name='Dinosaurs')
        RiskTextField.objects.create(name='Species', risk=r1, order=1)
        RiskDateTimeField.objects.create(name='First found', risk=r1, order=2)
        RiskEnumField.objects.create(name='Diet', possible_values='Carnivore|Herbivore|Omnivore', risk=r1, order=3)
        RiskNumberField.objects.create(name='Number of legs', risk=r1, order=4)

        # make a request and save the response for testing
        c = Client()
        self.response = c.get('/risks/1/').json()

    def test_data_length(self):
        """ The reponse should have three fields """
        self.assertEquals(len(self.response),3)

    def test_data_order(self):
        """ fields should be present in the json in the correct order """
        expected_order = ['Species', 'First found', 'Diet', 'Number of legs']
        received_order = [field['name'] for field in self.response['fields']]
        self.assertEquals(expected_order, received_order)

    def test_risk_name(self):
        self.assertEquals(self.response['name'], 'Dinosaurs')

    def test_risk_field_count(self):
        self.assertEquals(len(self.response['fields']), 4)

    def test_risk_text_field(self):
        expected_data = {'id': 1, 'name': 'Species', 'order': 1, 'type': RiskField.TEXT}
        self.assertEquals(self.response['fields'][0], expected_data)

    def test_risk_number_field(self):
        expected_data = {'id': 1, 'name': 'Number of legs', 'order': 4, 'type': RiskField.NUMBER}
        self.assertEquals(self.response['fields'][3], expected_data)

    def test_risk_datetime_field(self):
        expected_data = {'id': 1, 'name': 'First found', 'order': 2, 'type': RiskField.DATETIME}
        self.assertEquals(self.response['fields'][1], expected_data)

    def test_risk_enum_field(self):
        expected_data = {'id': 1, 'name': 'Diet', 'order': 3, 'type': RiskField.ENUM, 'possible_values': ['Carnivore', 'Herbivore', 'Omnivore']}
        self.assertEquals(self.response['fields'][2], expected_data)

class TestEmptyRisk(TestCase):

    def setUp(self):
        # create a Risk with no fields.
        r1 = Risk.objects.create(name='Dinosaurs')

        # make a request and save the response for testing
        c = Client()
        self.response = c.get('/risks/1/').json()

    def test_data(self):
        self.assertEquals(self.response['fields'], [])
