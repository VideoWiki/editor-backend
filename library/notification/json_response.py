from django.http import JsonResponse

def json_response(
		message,
        data,
        status

):
    return JsonResponse({
        'message': message,
        'data': '{}'.format(data),
        'status': status
    })
