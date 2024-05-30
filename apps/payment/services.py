from datetime import datetime, timezone
from uuid import uuid4

from django.db import transaction

from apps.loans.services import LoanService, LoanStatus
from apps.payment.models import Payment, PaymentDetail, PaymentStatus


class PaymentService:

	@staticmethod
	def get_payment(payment_id):
		return Payment.objects.get(external_id=payment_id)

	@staticmethod
	@transaction.atomic
	def create_payment(customer, amount, save=True):
		new_payment = Payment.objects.create(
			external_id=uuid4(),
			total_amount=amount,
			customer=customer,
			paid_at=datetime.now(timezone.utc),
			status=PaymentStatus.COMPLETED
		)
		if save:
			new_payment.save()
		return new_payment

	@staticmethod
	@transaction.atomic
	def make_rejected_payment(customer, amount, save=True):
		new_payment = Payment.objects.create(
			external_id=uuid4(),
			total_amount=amount,
			customer=customer,
			paid_at=datetime.now(timezone.utc),
			status=PaymentStatus.REJECTED
		)
		if save:
			new_payment.save()
		return new_payment

	@staticmethod
	@transaction.atomic
	def make_single_loan_payment(loan_id: str, payment: 'Payment', amount: float, save=True, omit_checks=False):
		loan = LoanService.get_loan(loan_id)
		if loan.status != LoanStatus.ACTIVE:
			raise ValueError('The loan is not active')

		loan_debt = loan.outstanding_balance
		amount_to_pay = loan_debt if loan_debt <= amount else amount

		payment_detail = PaymentDetail.objects.create(
			loan=loan,
			payment=payment,
			amount=amount_to_pay
		)

		if save:
			payment_detail.save()

		if not omit_checks:
			transaction.on_commit(loan.verify_balance_and_change_status)

		return payment_detail
