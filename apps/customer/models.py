from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime, timezone


class Customer(models.Model):
	__tablename__ = 'customers_customer'

	status = models.SmallIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(2)], help_text='1=Active, 2=Inactive')
	external_id = models.CharField(max_length=60, unique=True)
	score = models.DecimalField(max_digits=20, decimal_places=10, default=0, validators=[MinValueValidator(0)])
	preapproved_at = models.DateTimeField(null=True, blank=True, validators=[MaxValueValidator(limit_value=datetime.now(tz=timezone.utc))])

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	@property
	def total_available_credit(self):
		debt = self.score - self.current_outstanding_credit
		if debt < 0:
			return 0
		return debt

	@property
	def current_outstanding_credit(self):
		return self.loans.aggregate(models.Sum('outstanding_balance'))['outstanding_balance__sum']
