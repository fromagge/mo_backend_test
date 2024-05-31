from datetime import datetime, timedelta, timezone

from django.test import TestCase

from apps.customer.services import CustomerService
from apps.loans.services import LoanService
from apps.payment.models import PaymentStatus


def one_year_from_now():
	return datetime.now(timezone.utc) + timedelta(days=365)


class PaymentTestCase(TestCase):

	def setUp(self):
		customer = CustomerService.create_customer({
			'external_id': '123',
			'status': 1,
			'score': 6_500_000.50
		})
		LoanService.create_loan(customer.external_id, 1_000_000.00, {
			'external_id': '1',
			'maximum_payment_date': one_year_from_now(),
		})
		LoanService.change_load_status('1', 2)
		LoanService.create_loan(customer.external_id, 3_000_000.00, {
			'external_id': '2',
			'maximum_payment_date': one_year_from_now(),
		})
		LoanService.change_load_status('2', 2)

	def test_capture_payment_endpoint(self):

		response = self.client.post('/payment/', {
			'customer_external_id': '123',
			'amount': 2_000_000.00
		})
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['payment']['status'], PaymentStatus.COMPLETED)
		self.assertAlmostEqual(float(response.data['payment']['total_amount']), 2_000_000.00)
		self.assertEqual(len(response.data['payment_details']), 2)

		response = self.client.post('/payment/', {
			'customer_external_id': '123',
			'amount': 20_000_000.00
		})
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data['status'], PaymentStatus.REJECTED)
		self.assertAlmostEqual(float(response.data['payment_amount']), 20_000_000.00)
		self.assertEqual(response.data['customer_external_id'], '123')
