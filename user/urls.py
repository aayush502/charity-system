from django.urls import path
from .views import *

app_name='user'

urlpatterns=[
    path('login_register/', LoginOrRegister.as_view(), name="login_register"),
    path('register/', RegisterRequest.as_view(), name="register"),
    path('login/', LoginRequest.as_view(), name="login"),
    path('logout/', Logout.as_view()),
]