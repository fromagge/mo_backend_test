from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.authentication.models import CustomUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
	id = serializers.IntegerField()

	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)

		return token

	def validate(self, attrs):
		user_id = attrs.get("id")
		password = attrs.get("password")

		try:
			user = CustomUser.objects.get(id=user_id)
		except CustomUser.DoesNotExist:
			raise serializers.ValidationError("No user with this ID exists.")

		if not user.check_password(password):
			raise serializers.ValidationError("Incorrect password.")

		data = super().validate(attrs)
		return data


class CustomTokenObtainPairView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer
