from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from apps.loans.models import Loan, LoanStatus

from apps.customer.services import CustomerService


class LoanService:

	@staticmethod
	@transaction.atomic
	def create_loan(user_id: str, loan_amount: float, loan_details: dict):
		loan_external_id = loan_details.pop('external_id')

		if Loan.objects.filter(external_id=loan_external_id).exists():
			raise ValidationError('A loan with the same external id already exists')

		user = CustomerService.get_user_external_id(user_id)

		if user.total_available_credit < loan_amount:
			raise serializers.ValidationError({'details': 'The loan amount exceeds the available credit of the user'})

		loan = Loan.objects.create(
			external_id=loan_external_id,
			customer=user,
			amount=loan_amount,
			status=LoanStatus.PENDING,
			**loan_details
		)

		return loan

	@staticmethod
	@transaction.atomic
	def change_load_status(loan_id: str, status):
		loan = Loan.objects.get(external_id=loan_id)
		loan.change_status(status)
		return loan

	@staticmethod
	def get_loan(loan_id):
		try:
			return Loan.objects.get(external_id=loan_id)
		except Loan.DoesNotExist:
			raise NotFound({'details': 'The loan does not exist'})
