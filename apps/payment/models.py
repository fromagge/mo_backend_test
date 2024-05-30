from django.utils.translation import gettext_lazy as _
from django.db import models


class PaymentDetail(models.Model):
	__tablename__ = 'payments_payment_detail'

	payment = models.ForeignKey('payment.Payment', on_delete=models.CASCADE, related_name='details')
	loan = models.ForeignKey('loans.Loan', on_delete=models.CASCADE, related_name='payments')
	amount = models.DecimalField(max_digits=20, decimal_places=10)

	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)


class PaymentStatus(models.IntegerChoices):
	COMPLETED = 1, _('Completed')
	REJECTED = 2, _('Rejected')


class Payment(models.Model):
	__tablename__ = 'payments_payment'

	external_id = models.CharField(max_length=60, unique=True)
	total_amount = models.DecimalField(max_digits=20, decimal_places=10)
	status = models.SmallIntegerField(default=1, choices=PaymentStatus.choices)
	customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='payments')

	paid_at = models.DateTimeField(null=True, blank=True)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)
