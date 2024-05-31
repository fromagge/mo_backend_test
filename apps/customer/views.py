from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common import validate
from apps.customer.serializers import CustomerBasicSerializer, CustomerDetailSerializer
from apps.customer.services import CustomerService


class CustomerCreateView(APIView):

	@validate(CustomerBasicSerializer)
	def post(self, request, payload, *args, **kwargs):
		customer = CustomerService.create_customer(payload)

		serialized_data = CustomerBasicSerializer(customer)
		return Response(serialized_data.data, 201)


class CustomerDetailView(APIView):

	def get(self, request, external_id, *args, **kwargs):
		customer = CustomerService.get_user_external_id(external_id)

		serialized_data = CustomerDetailSerializer(customer)
		return Response(serialized_data.data, 200)


