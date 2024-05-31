from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common import validate
from apps.loans.serializers import LoanCreateSerializer, LoanDetailSerializer, LoanUpdateSerializer
from apps.loans.services import LoanService


class LoanCreateView(APIView):

	@validate(LoanCreateSerializer)
	def post(self, request, payload, *args, **kwargs):
		user_id = payload.pop('customer')
		loan_amount = payload.pop('amount')

		loan = LoanService.create_loan(user_id, loan_amount, payload)

		serialized_data = LoanDetailSerializer(loan)
		return Response(serialized_data.data, 201)


class LoanDetailView(APIView):

	def get(self, request, external_id, *args, **kwargs):
		loan = LoanService.get_loan(external_id)

		serialized_data = LoanDetailSerializer(loan)
		return Response(serialized_data.data, 200)

	@validate(LoanUpdateSerializer)
	def update(self, request, external_id, *args, **kwargs):
		loan = LoanService.change_load_status(external_id, request.data['status'])

		serialized_data = LoanDetailSerializer(loan)
		return Response(serialized_data.data, 200)