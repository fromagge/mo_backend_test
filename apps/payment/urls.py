from django.urls import path, include
from apps.payment.views import PaymentCreateView, PaymentDetailView

urlpatterns = [
	path('', PaymentCreateView.as_view(), name='capture_payment'),
	path('<str:external_id>/', PaymentDetailView.as_view(), name='detail_payment'),
]