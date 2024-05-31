from datetime import datetime, timezone
from uuid import uuid4

from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.loans.services import LoanService, LoanStatus
from apps.payment.models import Payment, PaymentDetail, PaymentStatus


class PaymentService:

	@staticmethod
	def get_payment(payment_id, include_details=False):
		try:
			payment = Payment.objects.get(external_id=payment_id)
			if include_details:
				payment_details = PaymentDetail.objects.filter(payment=payment).all()
				return payment, payment_details
			return payment
		except Payment.DoesNotExist:
			raise ValidationError({'details': 'The payment does not exist'})


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
			raise ValidationError('The loan is not active')

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
