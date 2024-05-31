from django.contrib import admin

from apps.authentication.models import CustomUser

# Register your models here.
admin.register(CustomUser)