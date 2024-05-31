from rest_framework import serializers

from apps.common import BaseSerializer
from apps.payment.models import Payment, PaymentDetail


class PaymentSerializer(BaseSerializer):
	class Meta:
		model = Payment
		fields = ['external_id', 'customer', 'total_amount', 'paid_at', 'status']


class PaymentDetailSerializer(BaseSerializer):
	external_id = serializers.CharField(source='payment.external_id')
	customer_external_id = serializers.CharField(source='payment.customer.external_id')
	loan_external_id = serializers.CharField(source='loan.external_id')
	payment_date = serializers.DateTimeField(source='payment.paid_at')
	status = serializers.CharField(source='payment.status')
	total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, source='payment.total_amount')
	amount = serializers.DecimalField(max_digits=12, decimal_places=2)

	class Meta:
		model = PaymentDetail
		fields = ['external_id', 'customer_external_id', 'loan_external_id', 'payment_date', 'status', 'total_amount', 'amount']


class PaymentRejectedDetailSerializer(BaseSerializer):
	payment_date = serializers.DateTimeField(source='paid_at')
	payment_amount = serializers.DecimalField(max_digits=12, decimal_places=2, source='total_amount')
	customer_external_id = serializers.CharField(source='customer.external_id')

	class Meta:
		model = Payment
		fields = ['external_id', 'customer_external_id', 'payment_date', 'status', 'total_amount', 'payment_amount']
		fields_to_be_removed = ['loan_external_id']


class PaymentCreateSerializer(BaseSerializer):
	amount = serializers.DecimalField(max_digits=12, decimal_places=2)
	customer_external_id = serializers.CharField()

	class Meta:
		model = Payment
		fields = ['amount', 'customer_external_id']
