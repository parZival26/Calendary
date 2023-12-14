from django.urls import path
from .views import Login, log_out, Register

    
urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", log_out, name="logout")
]
