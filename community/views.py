from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from .models import Subscriber, Volunteer
from library.mailchimp.send_mail import sendMail
from .serializer import contactSerializer
from rest_framework.response import Response


class ChainLink(APIView):
    def get(self, request, pk):
        return Response({"id": "1", 'rewards': 23, "metadata": "metadata 1"})

class add_subscribe(APIView):

    def post(self, request):
        email = request.data['email']

        try:
            email = Subscriber.objects.get(email=email)
            return JsonResponse({"message": "Email Already exists.", "status": status.HTTP_409_CONFLICT})

        except Subscriber.DoesNotExist:
            Subscriber.objects.create(email=email)
            name = email.split('@')[0]
            # sendMail(template_name, to_email, name)
            global_merge_vars = [
                {
                    'name': 'NAME',
                    'content': name,
                }

            ]
            subscribe_template = "Successfully Subscribed"
            subject = "Subscribed!"
            status_res = sendMail(subscribe_template, email, name, subject, global_merge_vars)
            return JsonResponse({"message": status_res, "status": status.HTTP_200_OK})


class add_volunteer(APIView):

    def post(self, request):
        name = request.data['name']
        email = request.data['email']
        contact = request.data['contact']
        # resume = request.POST.get('resume')
        description = request.data['description']

        try:
            email = Volunteer.objects.get(email=email)
            return JsonResponse({"message": "Email Already exists.", "status": status.HTTP_409_CONFLICT})

        except Volunteer.DoesNotExist:
            Volunteer.objects.create(
                name=name, email=email, contact=contact, description=description)

            global_merge_vars = [
                {
                    'name': 'NAME',
                    'content': name,
                }

            ]
            volunteer_template = "Applied to volunteer"
            subject = "Thanks For Volunteering!"
            status_res = sendMail(volunteer_template, email, name, subject, global_merge_vars)

            return JsonResponse({"message": status_res, "status": status.HTTP_200_OK})


class contactForm(APIView):

    def post(self, request):
        dataSerializer = contactSerializer(data=request.data)
        if dataSerializer.is_valid():
            dataSerializer.save()
            return Response({"message": "Successful", 'data': dataSerializer.data["id"], "status": True})
        return Response({"message": "Not Successful", "status": False})
