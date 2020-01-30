from django.urls import path, include

import hub.views

urlpatterns = [
    path("login", hub.views.login_page),
    path("auth", hub.views.validate_user),
]