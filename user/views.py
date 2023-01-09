from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from user.models import User, UserProfile
from user.serializers import UserSerializer, UserLoginSerializer
from user.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import serializers
from coutoEditor.global_variable import BASE_URL
from django.contrib.auth import authenticate
from .signals import send_otp_details
from django.utils.crypto import get_random_string
from rest_framework_jwt.settings import api_settings
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from uuid import uuid4
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


@api_view(['GET'])
def check_user(request):
    """
    check if user exists or not
    :param request:
    :type request:
    :return: true is user exists
    :rtype: bool
    """
    username = request.GET.get('username')
    email = request.GET.get('email')
    if not username and not email:
        return Response({
            'message': "username or email missing.",
        }, status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({
                'message': "email and username does not exists.",
            }, status.HTTP_400_BAD_REQUEST)

    return Response({
        'message': "username or email exists.",
    }, status.HTTP_200_OK)


class UserRegistrationView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        e1 = request.data['email']
        request.data['email'] = e1.lower()
        if User.objects.filter(email=request.data['email']).exists():
            return Response({
                "message":"account with this email already exists",
                "status": False
            },status=status.HTTP_400_BAD_REQUEST
            )
        # user_name = request.data["first_name"] + request.data["last_name"]
        # if User.objects.filter(username__iexact=user_name).exists():
        #     request.data['username'] = request.data["first_name"] + request.data["last_name"] + "-" + str(uuid4().hex[:30])
        # else:
        #     request.data['username'] = request.data["first_name"] + request.data["last_name"]


        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            try:
                if User.objects.filter(
                        email=(serializer.data['email']).lower()
                ).exists():
                    raise serializers.ValidationError("email already exists")
            except Exception as e:
                error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
                raise serializers.ValidationError(error)
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()

        user_obj = User.objects.get(
            email=serializer.data['email'].lower()
        )
        try:
            photo_url_obj = UserProfile.objects.get(user=user_obj).profile_image.url
            photo_url = BASE_URL[:-1] + photo_url_obj
        except:
            photo_url_obj = ""
            photo_url = photo_url_obj
        response = {
            'usersData': {
                "id": user_obj.id,
                "username": user_obj.username,
                "email": user_obj.email,
                "first_name": user_obj.first_name,
                "last_name": user_obj.last_name,
                "profile": {
                    "profile_image": photo_url,
                    "phone": serializer.data['profile']['phone'],
                    "date_of_birth": serializer.data['profile']['date_of_birth'],
                    "country": serializer.data['profile']['country'],
                    "city": serializer.data['profile']['city'],
                    "zip": serializer.data['profile']['zip'],
                    "active": serializer.data['profile']['active']
                }
            },
            'message': 'User registered successfully',
            'status': 'True',
        }
        status_code = status.HTTP_201_CREATED
        return Response(response, status=status_code)


class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = User.objects.get(
            email=(serializer.data['email']).lower()
        )
        try:
            photo_url_obj = UserProfile.objects.get(
                user=user_obj
            ).profile_image.url
            photo_url = BASE_URL[:-1] + photo_url_obj
        except:
            photo_url_obj = ""
            photo_url = photo_url_obj

        response = {
            'usersData': {
                "id": user_obj.id,
                "username": user_obj.username,
                "email":user_obj.email,
                "first_name": user_obj.first_name,
                "last_name": user_obj.last_name,
                "profile_image": photo_url},
            'message': 'User logged in successfully',
            'status': 'True',
            'accessToken': serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class ChangePasswordViewSet(RetrieveAPIView):

    permission_classes = (IsLoggedInUserOrAdmin,)

    def post(self, request):
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']
        current_password = request.data['current_password']

        #authenticate old password
        user = authenticate(username=request.user.username, password=current_password)
        if user is None:
            return Response(
                {"message": "current password didn't match!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password == confirm_password:
           # reset password
           request.user.set_password(confirm_password)
           request.user.save()
        else:
            return Response(
                {"message": "password didn't match !"},
                status = status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Password Reset Successful!"},
            status=status.HTTP_200_OK
        )


class UpdateUserProfile(RetrieveAPIView):

    permission_classes = (IsLoggedInUserOrAdmin,)

    def post(self, request):
        user = request.user
        validated_data = request.data
        profile = UserProfile.objects.get(
            user = request.user
        )
        username = validated_data.get('username', user.username)
        if user.username != username:
            user.username = validated_data.get('username', user.username)
            try:
                if User.objects.filter(
                        username__iexact=user.username
                ).exists():
                    return Response({
                        "message":"username already exist !"},
                        status = status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
                return Response({
                    "message": error },
                    status=status.HTTP_400_BAD_REQUEST
                )
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.email = validated_data.get('email', user.email)
        user.save()
        profile.profile_image = validated_data.get('profile_image', profile.profile_image)
        profile.phone = validated_data.get('phone', profile.phone)
        profile.date_of_birth = validated_data.get('date_of_birth', profile.date_of_birth)
        profile.country = validated_data.get('country', profile.country)
        profile.city = validated_data.get('city', profile.city)
        profile.zip = validated_data.get('zip', profile.zip)
        profile.active = validated_data.get('active', profile.active)
        profile.save()
        try:
            url = BASE_URL[:-1] + profile.profile_image.url
        except:
            url = ""
        return Response({
            "user_data":{"profile_image": url},
            'message':"user updated successfully !"},
            status=status.HTTP_200_OK
        )


class validate_email_Send_otp(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            email  = str(email)
            user = User.objects.filter(email__iexact = email)

            if user.exists():
                key = send_otp(email)

                if key:
                    old = User.objects.filter(email__iexact=email)
                    if old.exists():
                        old = old.first()
                        print(old)
                        count = old.count
                        # if count > 20:
                        #     return Response({
                        #         'status': False,
                        #         'detail' : 'Sending otp error. Limit Exceeded. Please contact customer support.'
                        #         })
                        old.count = count + 1
                        hashed_otp = make_password(key)
                        old.otp = hashed_otp
                        old.save()
                        print('Count Increase', count)
                        status_code = status.HTTP_200_OK
                        mail_status = send_otp_details(email, key)
                        return Response({
                            'message': 'otp sent successfully.',
                            'status': True,
                            'mail': mail_status }, status_code)
            else:
                key = send_otp(email)

                if key:
                    old = User.objects.filter(email__iexact = email)
                    if old.exists():
                        old  = old.first()
                        count = old.count
                        # if count > 20:
                        #     return Response({
                        #         'status': False,
                        #         'detail' : 'Sending otp error. Limit Exceeded. Please contact customer support.'
                        #         })
                        old.count = count + 1
                        # old.otp = key
                        hashed_otp = make_password(old)
                        old.save()
                        print('Count Increase', count)
                        status_code = status.HTTP_200_OK
                        mail_status = send_otp_details(email, key)
                        return Response({
                            'message': 'User registered successfully',
                            'status': True,
                            'detail': 'otp sent successfully.',
                            'mail': mail_status}, status_code)
                    else:
                        hashed_otp = make_password(key)
                        user = User.objects.create(
                            username = email,
                            email = email,
                            otp = hashed_otp,

                            )
                        profile = UserProfile.objects.create(user=user, active=True)
                        # link = f'API-urls'
                        # requests.get(link)
                        status_code = status.HTTP_200_OK
                        mail_status = send_otp_details(email, key)
                        return Response({
                            'message': 'User registered successfully',
                            'status': True,
                            'detail': 'otp sent successfully.',
                            'mail': mail_status
                            }, status_code)



                else:
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response({
                        'status' : False,
                        'detail' : 'Sending otp error.'
                        }, status_code)

        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({
                'status' : False,
                'detail' : 'email is not given in post request.'
                }, status_code)


def send_otp(email):
    if email:
        key = get_random_string(6, '0123456789')
        # otp = send_otp_details(email, key)
        # print(otp)
        return key
    else:
        return False


class validate_otp(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email' , False)
        otp_sent = request.data.get('otp', False)

        if email and otp_sent:
            old = User.objects.filter(email__iexact = email)
            if old.exists():
                old = old.first()
                otp = old.otp
                if check_password(otp_sent, otp):
                    old.validated = True
                    old.save()
                    try:
                        payload = JWT_PAYLOAD_HANDLER(old)
                        jwt_token = JWT_ENCODE_HANDLER(payload)
                        update_last_login(None, old)
                    except User.DoesNotExist:
                        raise serializers.ValidationError(
                            'user with given email and password does not exists'
                        )
                    user_obj = User.objects.get(
                        email=email
                    )
                    try:
                        photo_url_obj = UserProfile.objects.get(
                            user=user_obj
                        ).profile_image.url
                        photo_url = BASE_URL[:-1] + photo_url_obj
                    except:
                        photo_url_obj = ""
                        photo_url = photo_url_obj
                    response = {
                        'usersData': {
                            "id": user_obj.id,
                            "username": user_obj.username,
                            "email": user_obj.email,
                            "first_name": user_obj.first_name,
                            "last_name": user_obj.last_name,
                            "profile_image": photo_url},
                        'message': 'User logged in successfully',
                        'status': True,
                        'accessToken': jwt_token
                        # 'detail': 'otp mactched.'
                    }
                    status_code = status.HTTP_200_OK
                    return Response(response, status_code)

                else:
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response({
                        'status' : False,
                        'detail' : 'otp incorrect.'
                        }, status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response({
                    'status' : False,
                    'detail' : 'first proceed via sending otp request.'
                    }, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({
                'status' : False,
                'detail' : 'please provide both email and otp for validations'
                }, status_code)