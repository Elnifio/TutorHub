from django.shortcuts import render
from hub.models import User, Event
from django.http import HttpResponse, JsonResponse

# Create your views here.
def login_page(request):
    return render(request, 'hub/login.html', {})

def validate_user(request):
    request.encoding="utf-8"
    status = {"user": "", "status": False}
    if 'name' in request.GET and request.GET['name']:
        user_name = request.GET['name']
    else:
        return JsonResponse(status)
    # TODO
    return JsonResponse(status)