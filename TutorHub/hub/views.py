from django.shortcuts import render
from hub.models import User, Event
from django.http import HttpResponse

# Create your views here.
def login_page(request):
    return render(request, 'hub/login.html', {})