from datetime import datetime, timezone

from django.test import TestCase

from apps.customer.models import Customer


class CustomerTestCase(TestCase):
	def setUp(self):
		Customer.objects.create(status=1, external_id='123456', score=10_250_000.321)

	def test_customer_status(self):
		customer = Customer.objects.get(external_id="123456")
		self.assertEqual(customer.external_id, "123456")
		self.assertEqual(customer.status, 1)

	# Test endpoints

	def test_create_customer(self):
		response = self.client.post('/customer/', {'external_id': '123', 'status': 1, 'score': 10_250_000})

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['external_id'], '123')
		self.assertEqual(response.data['status'], 1)

		customer = Customer.objects.get(external_id='123')
		self.assertEqual(customer.external_id, '123')
		self.assertEqual(customer.status, 1)
		self.assertEqual(customer.score, 10_250_000)

		time_in_future = datetime.now(timezone.utc).replace(year=2025)
		response = self.client.post('/customer/', {'external_id': '123', 'status': 3, 'score': 10_250_000, 'preapproved_at': time_in_future})
		self.assertEqual(response.status_code, 400)

		self.assertIn('external_id', response.data)
		self.assertIn('status', response.data)
		self.assertIn('preapproved_at', response.data)
		self.assertNotIn('score', response.data)

	def test_get_customer(self):
		response = self.client.get('/customer/123456/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['external_id'], '123456')

		response = self.client.get('/customer/1234567/')
		self.assertEqual(response.status_code, 404)
		self.assertIn('details', response.data)
		self.assertEqual(response.data['details'], 'The user does not exist')




