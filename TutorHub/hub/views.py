from django.shortcuts import render, redirect
from hub.models import User, Event, Tag
from django.http import HttpResponse, JsonResponse
import json


unsafe_password = [
    '123456',
    'abcdef',
    'password'
]

# Create your views here.
def homepage(request):
    print(request.COOKIES)
    login_status = request.COOKIES.get('login', False)
    user_id = request.COOKIES.get('id', -1)
    return render(request, 'hub/homepage.html', {
        "login": login_status, 
        "event_counts": range(Event.objects.all().count()),
        "events": Event.objects.all()
    })


def login_page(request):
    return render(request, 'hub/login.html', {})


def logout(request):
    if request.COOKIES.get('login', False):
        response = render(request, 'hub/homepage.html', {
            'login': False,
            "event_counts": range(Event.objects.all().count()),
            "events": Event.objects.all()
        })
        response.delete_cookie('login')
        response.delete_cookie('id')
        return response
    else:
        return render(request, 'hub/homepage.html', {
            'login': False,
            "event_counts": range(Event.objects.all().count()),
            "events": Event.objects.all()
        })


def register_page(request):
    return render(request, 'hub/register.html', {
        'no_name': False,
        "empty_password": False,
        "invalid_password": False,
        'not_match': False,
        'no_email': False
    })


def register_user(request):
    user_name = ""
    user_email = ""
    password = ""

    no_name = False
    empty_password = False
    invalid_password = False
    not_match = False
    no_email = False

    if not ('name' in request.GET and request.GET['name']):
        no_name = True
    if not ('pwd' in request.GET and request.GET['pwd']):
        empty_password = True
    elif request.GET['pwd'] in unsafe_password:
        invalid_password = True
    
    if not ("confirm" in request.GET and request.GET['confirm']):
        not_match = True
    elif not request.GET['pwd'] == request.GET['confirm']:
        not_match = True
    
    if not ('email' in request.GET and request.GET['email']):
        no_email = True

    if not (not no_name and not empty_password and not invalid_password and not not_match):
        return render(request, 'hub/register.html', {
            'no_name': no_name,
            'empty_password': empty_password,
            'invalid_password': invalid_password,
            'not_match': not_match,
            'no_email': no_email,
            "multiple_email": False,
        })

    # TODO change this url to register page 2
    response = render(request, 'hub/homepage.html', {
        'login': True,
        "event_counts": range(Event.objects.all().count()),
        "events": Event.objects.all()
    })
    if not 'login' in request.COOKIES:
        response.set_cookie('login', False)
    if not 'username' in request.COOKIES:
        response.set_cookie('username', "")

    user_name = request.GET['name']
    password = request.GET['pwd']
    user_email = request.GET['email']
    if User.objects.filter(email=user_email):
        return render(request, 'hub/register.html', {
            'no_name': no_name,
            'empty_password': empty_password,
            'invalid_password': invalid_password,
            'not_match': not_match,
            'no_email': no_email,
            "multiple_email": True,
        })
    user = User()
    user.username = user_name
    user.password = password
    user.email = user_email
    user.save()
    response.set_cookie('login', True)
    response.set_cookie('id', user.user_id)
    return response
    

def validate_user(request):
    # print(request.COOKIES)
    # print(request.session)
    # status = {"user": "", "status": False}
    # print("Query Dict: ")
    # print(request.GET)
    user_name = ""
    password = ""
    if 'email' in request.GET and request.GET['email']:
        user_email = request.GET['email']
    else:
        return render(request, 'hub/loginFail.html', {
            "error_msg": "Please provide user name. "
        })
    
    if 'pwd' in request.GET and request.GET['pwd']:
        password = request.GET['pwd']
    else:
        return render(request, 'hub/loginFail.html', {
            "error_msg": "Please provide password."
        })
    
    if not User.objects.all().filter(email=user_email).exists():
        return render(request, 'hub/loginFail.html', {
            'error_msg': "Cannot find user."
        })
    
    user = User.objects.get(email=user_email)
    if not password == user.password:
        return render(request, 'hub/loginFail.html', {
            'error_msg': "Username or password error."
        })
    
    response = render(request, 'hub/homepage.html', {
        'login': True,
        "event_counts": range(Event.objects.all().count()),
        "events": Event.objects.all()
    })
    response.set_cookie('login', True)
    response.set_cookie('id', user.user_id)
    return response


def create_event(request):
    event_name = ""
    event_date = ""
    event_description = ""

    no_name = False
    no_date = False
    no_description = False
    no_tags = False
    no_hoster = False
    no_location = False
    no_poster = False
    no_poster_continue = False

    if not ('name' in request.GET and request.GET['name']):
        no_name = True
    if not ('date' in request.GET and request.GET['date']):
        no_date = True
    if not ("description" in request.GET and request.GET['description']):
        no_description = True
    if not ('tags' in request.GET and request.GET['tags']):
        no_tags = True
    if not ('hoster' in request.GET and request.GET['hoster']):
        no_hoster = True
    if not ('location' in request.GET and request.GET['location']):
        no_location = True
    if not ('poster' in request.GET and request.GET['poster']):
        no_poster = True

    if not (not no_name and not no_date and not no_description and not no_tags and not no_hoster and not no_location):
        return render(request, 'hub/createEvent.html', {
            'no_name': no_name,
            'no_date': no_date,
            'no_description': no_description,
            'no_tags': no_tags,
            'no_hoster': no_hoster,
            'no_location': no_location,
            'no_poster': no_poster,
        })

    event = Event()
    event.name = request.GET['name']
    event.date = request.GET['date']
    event.description = request.GET['description']
    tags = request.GET['tags'].replace(" ", "").split(",")
    tag_list = []
    for tag in tags: 
        tag = tag.lower()
        if not Tag.objects.filter(tag_name=tag):
            t = Tag()
            t.tag_name = tag
            t.save()
        tag_list.append(tag)
    event.tags = json.dumps(tag_list)
        

    
    