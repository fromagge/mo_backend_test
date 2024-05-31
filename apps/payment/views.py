from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common import validate
from apps.customer.services import CustomerService
from apps.payment.models import PaymentStatus
from apps.payment.serializers import PaymentCreateSerializer, PaymentSerializer, PaymentRejectedDetailSerializer, PaymentDetailSerializer
from apps.payment.services import PaymentService


class PaymentCreateView(APIView):

	@validate(PaymentCreateSerializer)
	def post(self, request, payload, *args, **kwargs):
		customer_external_id = payload.pop('customer_external_id')
		amount = payload.pop('amount')

		payment, payment_details = CustomerService.make_payment(customer_external_id, amount)

		if payment.status == PaymentStatus.REJECTED:
			serialized_data = PaymentRejectedDetailSerializer(payment)
			return Response(serialized_data.data, 400)
		else:
			return Response({
				'payment': PaymentSerializer(payment).data,
				'payment_details': PaymentDetailSerializer(payment_details, many=True).data
			}, 201)


class PaymentDetailView(APIView):

	def get(self, request, external_id, *args, **kwargs):
		payment, payment_details = PaymentService.get_payment(external_id, include_details=True)

		return Response({
			'payment': PaymentSerializer(payment).data,
			'payment_details': PaymentDetailSerializer(payment_details, many=True).data
		}, 200)
