from datetime import timezone, datetime

from rest_framework import serializers

from apps.common import BaseSerializer
from apps.customer.serializers import CustomerDetailSerializer
from apps.loans.models import Loan


class LoanCreateSerializer(BaseSerializer):
	customer_external_id = serializers.CharField(source='customer')

	class Meta:
		model = Loan
		fields = ['external_id', 'customer_external_id', 'amount', 'maximum_payment_date']
		required_fields = ['external_id', 'customer_external_id', 'amount', 'maximum_payment_date']

		def validate(self, data):
			if data['amount'] <= 0:
				raise serializers.ValidationError({'amount': 'Loan amount should be greater than 0'})

			if data['maximum_payment_date'] <= datetime.now(timezone.utc):
				raise serializers.ValidationError({'maximum_payment_date': 'Maximum payment date should be greater than current date'})

			return data


class LoanDetailSerializer(BaseSerializer):
	outstanding_balance = serializers.DecimalField(max_digits=12, decimal_places=2)
	customer_external_id = serializers.CharField(source='customer.external_id')

	class Meta:
		model = Loan
		fields = ['external_id', 'customer_external_id', 'amount', 'outstanding_balance', 'contract_version', 'status']
		fields_to_be_removed = ['contract_version']
