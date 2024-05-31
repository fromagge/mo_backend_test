from django.urls import path, include
from apps.loans.views import LoanCreateView, LoanDetailView

urlpatterns = [
	path('', LoanCreateView.as_view(), name='create_loan'),
	path('<str:external_id>/', LoanDetailView.as_view(), name='get_loan'),

]