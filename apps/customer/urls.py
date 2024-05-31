from django.urls import path, include

from apps.customer.views import CustomerCreateView, CustomerDetailView, CustomerLoansListView

urlpatterns = [
	path('', CustomerCreateView.as_view(), name='create_customer'),
	path('<str:external_id>/', CustomerDetailView.as_view(), name='get_customer'),
	path('<str:external_id>/loans', CustomerLoansListView.as_view(), name='list_loans')
]