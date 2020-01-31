from django.shortcuts import render
from hub.models import User, Event
from django.http import HttpResponse, JsonResponse

unsafe_password = [
    '123456',
    'abcdef',
    'password'
]

# Create your views here.
def homepage(request):
    if not 'login' in request.COOKIES:
        request.COOKIES["login"] = False
    return render(request, 'hub/homepage.html', {
        "login": request.COOKIES['login']
    })


def login_page(request):
    return render(request, 'hub/login.html', {})


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
            'no_email': no_email
        })

    user_name = request.GET['name']
    password = request.GET['pwd']
    user_email = request.GET['email']
    


def validate_user(request):
    # print(request.COOKIES)
    # print(request.session)
    # status = {"user": "", "status": False}
    # print("Query Dict: ")
    # print(request.GET)
    user_name = ""
    password = ""
    if 'name' in request.GET and request.GET['name']:
        user_name = request.GET['name']
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
    
    if not User.objects.all().filter(username=user_name).exists():
        return render(request, 'hub/loginFail.html', {
            'error_msg': "User does not exist."
        })
    
    user = User.objects.get(username=user_name)
    if not password == user.password:
        return render(request, 'hub/loginFail.html', {
            'error_msg': "Username or password error."
        })
    
    request.COOKIES['login'] = True
    return render(request, 'hub/homepage.html', {
        'login': True
    })