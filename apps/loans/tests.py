from datetime import datetime, timedelta, timezone
from uuid import uuid4

from django.test import TestCase

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

	def test_create_loan(self):
		customer = Customer.objects.get(external_id="1")

		# Let's create a loan an make sure it's active

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
