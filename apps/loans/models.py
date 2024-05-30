from datetime import timezone, datetime

from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.payment.models import PaymentStatus, PaymentDetail


class LoanStatus(models.IntegerChoices):
	PENDING = 1, _("Pending")
	ACTIVE = 2, _("Active")
	REJECTED = 3, _("Rejected")
	PAID = 4, _("Paid")


class Loan(models.Model):
	__tablename__ = 'loans_loan'

	external_id = models.CharField(max_length=60, unique=True)
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.SmallIntegerField(choices=LoanStatus.choices, default=LoanStatus.PENDING)
	contract_version = models.CharField(max_length=30, null=True, blank=True)
	maximum_payment_date = models.DateTimeField()
	taken_at = models.DateTimeField(null=True)
	customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='loans')

	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	@property
	def outstanding_balance(self):
		if self.status == LoanStatus.PAID or self.status == LoanStatus.REJECTED:
			return 0

		total_payments = self.completed_payments().aggregate(models.Sum('amount'))

		if not total_payments or not total_payments['amount__sum']:
			return self.amount

		return self.amount - total_payments['amount__sum']

	def completed_payments(self):
		return PaymentDetail.objects.filter(loan_id=self, payment__status=PaymentStatus.COMPLETED).all()

	def all_payments(self):
		return PaymentDetail.objects.filter(loan_id=self, payment__status=PaymentStatus.COMPLETED).all()

	def activate_loan(self):
		return self.change_status(LoanStatus.ACTIVE)

	def change_status(self, status):
		match self.status:
			case LoanStatus.ACTIVE:
				if status == LoanStatus.PAID:
					if self.outstanding_balance == 0:
						self.status = LoanStatus.PAID
						self.save()
				return
			case LoanStatus.PENDING:
				if status == LoanStatus.ACTIVE:
					self.status = LoanStatus.ACTIVE
					self.taken_at = datetime.now(timezone.utc)
					self.save()
				elif status == LoanStatus.REJECTED:
					self.status = LoanStatus.REJECTED
					self.save()
				return
			case _:
				return False

	def verify_balance_and_change_status(self):
		if self.outstanding_balance == 0:
			self.change_status(LoanStatus.PAID)
		else:
			self.change_status(LoanStatus.ACTIVE)
