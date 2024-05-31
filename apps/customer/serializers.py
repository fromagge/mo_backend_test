from datetime import datetime, timezone
from apps.common import BaseSerializer, serializers
from apps.customer.models import Customer


class CustomerBasicSerializer(BaseSerializer):
	score = serializers.DecimalField(max_digits=20, decimal_places=3)

	class Meta:
		model = Customer
		fields = ('external_id', 'status', 'score', 'preapproved_at')
		required_fields = ('external_id', 'status', 'score')
		fields_to_be_removed = ('preapproved_at',)

		def validate_score(self, value):
			print(value)
			if value < 0:
				raise serializers.ValidationError("The score must be a positive.")
			return value

		def validate_status(self, value):
			if value not in [1, 2]:
				raise serializers.ValidationError("The status must be either 1 (Active) or 2 (Inactive)")
			return value

		def validate_preapproved_at(self, value):
			if value is not None and value > datetime.now(timezone.utc):
				raise serializers.ValidationError("The preapproved_at date must be in the past.")
			return value


class CustomerDetailSerializer(serializers.ModelSerializer):
	total_debt = serializers.FloatField(source='current_outstanding_credit')
	available_amount = serializers.FloatField(source='total_available_credit')

	class Meta:
		model = Customer
		fields = ('external_id', 'status', 'score', 'total_debt', 'available_amount')
