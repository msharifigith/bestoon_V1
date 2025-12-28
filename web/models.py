from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.


class income(models.Model):
    image = models.ImageField(default='media/all_image/2.jpg', upload_to='media/all_image/', blank=True, )
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    time = models.DateField(auto_now_add=True)
    amount = models.BigIntegerField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.time}-{self.amount}"


class out(models.Model):
    image = models.ImageField(default='media/all_image/2.jpg', upload_to='media/all_image/', blank=True, )
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    time = models.DateField(auto_now_add=True)
    amount = models.BigIntegerField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.time}-{self.amount}"


class token(models.Model):
    token = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
