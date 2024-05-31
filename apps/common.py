from rest_framework import status, serializers
from functools import wraps
from rest_framework.response import Response


# Base classes
class BaseSerializer(serializers.ModelSerializer):

	# Used to remove fields from the response if they are None
	def to_representation(self, instance):
		rep = super().to_representation(instance)
		if hasattr(self.Meta, 'fields_to_be_removed'):
			for field in self.Meta.fields_to_be_removed:
				try:
					if rep[field] is None:
						rep.pop(field)
				except KeyError:
					pass
		return rep


# Decorators
def validate(serializer_class):
	def decorator(func):
		@wraps(func)
		def wrapped(self, request, *args, **kwargs):
			serializer = serializer_class(data=request.data)
			if serializer.is_valid():
				return func(self, request, serializer.validated_data, *args, **kwargs)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		return wrapped

	return decorator
