from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField()
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of opt_sent')
    nonce = models.CharField(max_length=500)
    token_string = models.CharField(blank=True, null=True, max_length=32)
    validated = models.BooleanField(default=False,
                                    help_text='if it is true, that means user have validate otp correctly in seconds')
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    profile_image = models.ImageField(blank=True, upload_to='user/profile_img', null=True,default=None)
    phone = models.CharField( max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=15, null=True, blank=True)
    active = models.BooleanField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')