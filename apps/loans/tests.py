from datetime import datetime, timedelta, timezone
from uuid import uuid4

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from apps.authentication.models import CustomUser
from apps.customer.models import Customer
from apps.customer.services import CustomerService
from apps.loans.models import LoanStatus, Loan
from apps.loans.services import LoanService
from apps.payment.models import PaymentStatus
from apps.payment.services import PaymentService


def one_year_from_now():
	return datetime.now(timezone.utc) + timedelta(days=365)


class CustomerTestCase(TestCase):
	def setUp(self):
		Customer.objects.create(external_id='1', score=10_250_000.321)
		Customer.objects.create(external_id='2', score=10_250_000.321)

		# Authentication

		CustomUser.objects.create_user('testo', 'myemail@test.com', 'password', id="1", is_staff=True)
		self.client = APIClient()
		response = self.client.post(reverse('get_token'), {
			'id': '1',
			'username': "testo",
			'password': 'password'
		}, format='json')
		self.token = response.data['access']
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

	def test_create_loan(self):
		customer = Customer.objects.get(external_id="1")

		# Let's create a loan and make sure it's active

		loan_amount = 5_000_000
		loan_external_id = '1'

		LoanService.create_loan(user_id=customer.external_id, loan_amount=loan_amount, loan_details={
			'external_id': loan_external_id,
			'maximum_payment_date': one_year_from_now()
		})

		self.assertEqual(customer.loans.count(), 1)
		self.assertEqual(customer.active_loans.count(), 0)

		loan = LoanService.change_load_status(loan_id=loan_external_id, status=LoanStatus.ACTIVE)

		self.assertEqual(customer.loans.count(), 1)
		self.assertEqual(customer.active_loans.count(), 1)
		self.assertEqual(customer.total_available_credit, customer.score - loan_amount)
		self.assertIsNotNone(loan.taken_at)

		# Let's create another loan make sure it's rejected

		time = one_year_from_now()
		LoanService.create_loan(user_id=customer.external_id, loan_amount=loan_amount, loan_details={
			'external_id': '222',
			'maximum_payment_date': time
		})

		loan = LoanService.change_load_status(loan_id='222', status=LoanStatus.REJECTED)
		self.assertEqual(customer.loans.count(), 2)
		self.assertEqual(customer.active_loans.count(), 1)
		self.assertEqual(loan.external_id, '222')
		self.assertEqual(loan.status, LoanStatus.REJECTED)
		self.assertEqual(loan.maximum_payment_date, time)
		self.assertIsNone(loan.taken_at)

	def test_outstanding_balance(self):
		customer = Customer.objects.get(external_id="1")
		loan = LoanService.create_loan(user_id=customer.external_id, loan_amount=5_000_000, loan_details={
			'external_id': "1",
			'maximum_payment_date': one_year_from_now()
		})
		LoanService.change_load_status(loan_id=loan.external_id, status=LoanStatus.ACTIVE)
		self.assertEqual(loan.outstanding_balance, 5_000_000)

		# Let's make a payment
		payment = PaymentService.create_payment(customer=customer, amount=1_000_000)
		PaymentService.make_single_loan_payment(loan_id=loan.external_id, payment=payment, amount=1_000_000)

		self.assertEqual(loan.outstanding_balance, 4_000_000)

		# Let's make another payment

		payment = PaymentService.create_payment(customer=customer, amount=500_000)
		PaymentService.make_single_loan_payment(loan_id=loan.external_id, payment=payment, amount=500_000)
		self.assertEqual(loan.outstanding_balance, 3_500_000)

		# Let's make another payment but failed
		payment = PaymentService.create_payment(customer=customer, amount=500_000)
		payment.status = PaymentStatus.REJECTED
		payment.save()
		PaymentService.make_single_loan_payment(loan_id=loan.external_id, payment=payment, amount=500_000)
		self.assertEqual(loan.outstanding_balance, 3_500_000)

	def create_loan_test(self, amount, status, customer):
		return Loan.objects.create(
			external_id=uuid4(),
			amount=amount,
			status=status,
			maximum_payment_date=one_year_from_now(),
			customer=customer
		)

	def test_total_available_credit_calculation(self):
		customer = Customer.objects.get(external_id="1")
		self.assertEqual(customer.total_available_credit, customer.score)

		self.create_loan_test(5_000_000, LoanStatus.ACTIVE, customer)
		self.assertEqual(customer.total_available_credit, customer.score - 5_000_000)

		self.create_loan_test(1_000_000, LoanStatus.ACTIVE, customer)
		self.assertEqual(customer.total_available_credit, customer.score - 5_000_000 - 1_000_000)

		self.create_loan_test(1_000_000, LoanStatus.PENDING, customer)
		self.create_loan_test(10_000_000, LoanStatus.REJECTED, customer)
		self.assertEqual(customer.total_available_credit, customer.score - 5_000_000 - 1_000_000)

		# Let's make a payment
		CustomerService.make_payment(external_id=customer.external_id, amount=4_000_000)
		self.assertEqual(customer.total_available_credit, customer.score - 2_000_000)

	# Let's test the endpoints

	def test_create_loan_endpoint(self):
		response = self.client.post('/loan/', {'external_id': '145', 'customer_external_id': '2', 'amount': 5_000_000.0, 'maximum_payment_date': one_year_from_now()})
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['customer_external_id'], '2')
		self.assertEqual(float(response.data['amount']), 5_000_000.0)
		self.assertEqual(response.data['status'], LoanStatus.PENDING)

		response = self.client.post('/loan/', {'external_id': '2', 'customer_external_id': '2', 'amount': 11_000_000.0, 'maximum_payment_date': one_year_from_now()})
		self.assertEqual(response.status_code, 400)
		self.assertIn('details', response.data)
		self.assertEqual(response.data['details'], 'The loan amount exceeds the available credit of the user')

	def test_get_loan_endpoint(self):
		Loan.objects.create(external_id='1', amount=9_000_000, status=LoanStatus.ACTIVE, maximum_payment_date=one_year_from_now(), customer=Customer.objects.get(external_id='2'))
		response = self.client.get('/loan/1/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['customer_external_id'], '2')
		self.assertEqual(float(response.data['amount']), 9_000_000)

		response = self.client.get('/loan/3/')
		self.assertEqual(response.status_code, 404)
		self.assertIn('details', response.data)
		self.assertEqual(response.data['details'], 'The loan does not exist')
