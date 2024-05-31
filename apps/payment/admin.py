from django.contrib import admin

from apps.payment.models import PaymentDetail, Payment

# Register your models here.
admin.register(Payment)
admin.register(PaymentDetail)
