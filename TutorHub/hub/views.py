from django.shortcuts import render, redirect
from hub.models import User, Event
from django.http import HttpResponse, JsonResponse

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