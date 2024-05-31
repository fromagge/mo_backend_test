from rest_framework import permissions


class UserIsOwner(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		match type(obj).__class__.__name__:
			case 'Loan':
				return obj.customer == request.user
			case 'Payment':
				return obj.customer == request.user
			case 'PaymentDetail':
				return obj.payment.customer == request.user
			case 'Customer':
				return obj.external_id == request.user.id or obj.id == request.user.id
			case _:
				return False
