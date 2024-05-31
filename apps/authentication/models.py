from datetime import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	is_staff = models.BooleanField(default=False)

