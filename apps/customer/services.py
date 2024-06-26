from django.db import transaction
from rest_framework.exceptions import ValidationError, NotFound

from apps.customer.models import Customer


class CustomerService:

	@staticmethod
	def get_user(external_id: str):
		return Customer.objects.get(id=external_id)

	@staticmethod
	def get_user_external_id(external_id: str):
		try:
			return Customer.objects.get(external_id=external_id)
		except Customer.DoesNotExist:
			raise NotFound({'details': 'The user does not exist'})

	@staticmethod
	@transaction.atomic
	def make_payment(external_id: str, amount: float):
		from apps.payment.services import PaymentService

		customer = CustomerService.get_user_external_id(external_id)
		if customer.active_loans.count() < 1:
			raise ValidationError('The user does not have any active loans')

		debt = customer.current_outstanding_credit
		# If the amount that the user is trying to pay is greater than the debt,
		#  we will not allow the payment to be made
		if amount > debt:
			return PaymentService.make_rejected_payment(customer=customer, amount=amount), None

		# If the amount is not greater we will start making payments on his loan until the amount is paid
		remaining_amount = amount
		active_loans = customer.active_loans.all()

		# Let's create a payment associated with the transaction
		payment = PaymentService.create_payment(customer=customer, amount=amount)

		# Let's iterate through the active loans and make payments on them
		payment_details = []
		for loan in active_loans:
			if remaining_amount <= 0:
				break

			payment_detail = PaymentService.make_single_loan_payment(loan_id=loan.external_id, payment=payment, amount=remaining_amount, save=False)
			payment_details.append(payment_detail)
			remaining_amount -= payment_detail.amount

		# Let's save the payment details
		for payment_detail in payment_details:
			payment_detail.save()

		return payment, payment_details

	@staticmethod
	def create_customer(payload, save=True):
		external_id = payload.pop('external_id')
		if Customer.objects.filter(external_id=external_id).exists():
			raise ValidationError('The customer already exists')

		customer = Customer.objects.create(external_id=external_id, **payload)

		if save:
			customer.save()

		return customer

	@staticmethod
	def get_customer_loans(external_id: str, only_active: bool = True):
		customer = CustomerService.get_user_external_id(external_id)
		if only_active:
			return customer.active_loans.all()

		return customer.all_loans.all()
