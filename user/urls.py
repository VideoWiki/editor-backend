from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from user.views import UserViewSet, check_user, UserLoginView,\
    UserRegistrationView, ChangePasswordViewSet, UpdateUserProfile, \
    validate_email_Send_otp, validate_otp
from user.password_reset.password_reset import SendResetMail, ResetPassword
from user.google_auth.google_login import GoogleView
from user.metamask.add_user import AddUser
from user.metamask.verify_signature import VerifySignature

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/verify-user/', check_user),
    url(r'^signup/', UserRegistrationView.as_view()),
    url(r'^signin/', UserLoginView.as_view()),
    url(r'change_password/', ChangePasswordViewSet.as_view()),
    url(r'user/update/', UpdateUserProfile.as_view()),
    url(r'send_otp/', validate_email_Send_otp.as_view()),
    url(r'validate_otp/', validate_otp.as_view()),
    url(r'password/reset/mail/', SendResetMail.as_view()),
    url(r'password/reset/', ResetPassword.as_view()),
    path('google/', GoogleView.as_view()),
    path('add/public/address/', AddUser.as_view()),
    path('verify/signature/', VerifySignature.as_view())
    ]
