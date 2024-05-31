from django.urls import path

from rest_framework_simplejwt.views import (
	TokenRefreshView
)

from apps.authentication.views import CustomTokenObtainPairView

urlpatterns = [
	path('token/', CustomTokenObtainPairView.as_view(), name='get_token'),
	path('token/refresh/', TokenRefreshView.as_view(), name='get_refresh_token'),
]
