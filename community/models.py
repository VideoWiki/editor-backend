from django.db import models
from django.utils import timezone


class Subscriber(models.Model):
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email


class Volunteer(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254)
    contact = models.CharField(max_length=20, null=True, blank=True)
    resume = models.FileField(upload_to="temporary/%Y/%m/%d")
    description = models.CharField(max_length=2000)
    joined_at = models.DateTimeField(
        default=timezone.datetime.utcnow, blank=True, null=True)

    def __str__(self):
        return self.email


class contactUs(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=50, blank=False)
    message = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email