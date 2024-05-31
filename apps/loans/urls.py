from django.urls import path, include
from apps.loans.views import LoanCreateView, LoanDetailView

urlpatterns = [
	path('', LoanCreateView.as_view(), name='create_loan'),
	path('<str:external_id>/', LoanDetailView.as_view(), name='get_loan'),
	path('<str:external_id>/status/', LoanDetailView.as_view(), name='update_loan_status'),
]