from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common import validate
from apps.customer.serializers import CustomerBasicSerializer, CustomerDetailSerializer
from apps.customer.services import CustomerService
from apps.loans.serializers import LoanDetailSerializer
from apps.permissions import UserIsOwner
from apps.utils import str_to_bool


class CustomerCreateView(APIView):
	permission_classes = [IsAdminUser]

	@validate(CustomerBasicSerializer)
	def post(self, request, payload, *args, **kwargs):
		customer = CustomerService.create_customer(payload)

		serialized_data = CustomerBasicSerializer(customer)
		return Response(serialized_data.data, 201)


class CustomerDetailView(APIView):
	permission_classes = [IsAdminUser, UserIsOwner]

	def get(self, request, external_id, *args, **kwargs):
		customer = CustomerService.get_user_external_id(external_id)

		self.check_object_permissions(request, customer)

		serialized_data = CustomerDetailSerializer(customer)
		return Response(serialized_data.data, 200)


class CustomerLoansListView(APIView):
	permission_classes = [IsAdminUser, UserIsOwner]

	def get(self, request, external_id, *args, **kwargs):
		only_active = str_to_bool(request.query_params.get('only_active', True))

		loans = CustomerService.get_customer_loans(external_id, only_active)

		serialized_data = LoanDetailSerializer(loans, many=True)
		return Response(serialized_data.data, 200)

