from user.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from ..signals import send_reset_mail
from django.utils.crypto import get_random_string
from coutoEditor.global_variable import VW_B_URL
from django.contrib.auth.hashers import make_password


class SendResetMail(APIView):
    def get(self, request):
        email = request.GET.get("email")
        origin = request.GET.get("origin")
        try:
            user_obj = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid emaiil"
            }, status=status.HTTP_400_BAD_REQUEST)
        rand_str = get_random_string(length=32)
        if origin == "cast":
            type = "?origin=cast"
        elif origin == "editor":
            type = "?origin=editor"
        reset_url = VW_B_URL + "password/reset/" + rand_str + f"/{origin}"
        user_obj.token_string = rand_str
        user_obj.save()
        mail_status = send_reset_mail(email, reset_url)
        return Response({
            "status": True,
            "reset_mail_status": mail_status
        })


class ResetPassword(APIView):
    def post(self, request):
        password = request.data["password"]
        token_string = request.data["token_string"]
        try:
            user_obj = User.objects.get(token_string=token_string)
        except ObjectDoesNotExist:
            return Response({
                "status": False,
                "message": "invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)
        user_obj_token = user_obj.token_string
        if user_obj_token == token_string:
            user_obj.password = make_password(password)
            rand_str = get_random_string(length=32)
            user_obj.token_string = rand_str
            user_obj.save()
            return Response({
                "status": True,
                "message": "password updated successfully"
            })
        else:
            return Response({
                "status": False,
                "message": "invalid token"
            }, status = status.HTTP_400_BAD_REQUEST)
