from django.utils.translation import gettext_lazy as _
from django.db import models


class Loan(models.Model):
	__tablename__ = 'loans_loan'

	class LoanStatus(models.TextChoices):
		PENDING = 1, _('Pending')
		ACTIVE = 2, _('Active')
		REJECTED = 3, _('Rejected')
		PAID = 4, _('Paid')

	external_id = models.CharField(max_length=60, unique=True)
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.SmallIntegerField(max_length=2, choices=LoanStatus.choices, default=LoanStatus.PENDING)
	contract_version = models.CharField(max_length=30, null=True, blank=True)
	maximum_payment_date = models.DateTimeField()
	taken_at = models.DateTimeField(null=True)
	customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='loans')

	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	@property
	def outstanding_balance(self):
		return 0
