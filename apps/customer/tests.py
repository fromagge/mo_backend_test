from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.customer.models import Customer


class CustomerTestCase(TestCase):
	def setUp(self):
		Customer.objects.create(status=1, external_id='123456', score=10_250_000.321)

	def test_customer_status(self):
		customer = Customer.objects.get(external_id="123456")
		self.assertEqual(customer.external_id, "123456")

