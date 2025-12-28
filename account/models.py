from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    profile = models.ImageField(upload_to='media/profile/', default='media/profile/user_default.jpg', blank=True)
