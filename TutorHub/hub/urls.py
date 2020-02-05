from django.urls import path, include
from django.conf.urls.static import static

import hub.views

urlpatterns = [
    path('', hub.views.homepage, name="homepage"),
    path("login", hub.views.login_page, name="login"),
    path("auth", hub.views.validate_user, name="auth"),
    path("register", hub.views.register_page, name="register"),
    path("register_page_2", hub.views.register_user, name="register_step_2"),
    path('logout', hub.views.logout, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)