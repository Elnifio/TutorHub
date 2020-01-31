from django.urls import path, include

import hub.views

urlpatterns = [
    path('', hub.views.homepage, name="homepage"),
    path("login", hub.views.login_page, name="login"),
    path("auth", hub.views.validate_user, name="auth"),
]