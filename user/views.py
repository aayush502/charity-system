from django.contrib import auth
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import *
import pdb
from django.contrib.auth.views import LoginView

class RegisterRequest(View):
    def get(self, request):
        form = NewUserForm()
        return render(request, 'user/register.html', context={"form":form})
    
    def post(self, request):
        user = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1==pass2:
            password = make_password(pass1)
            reg = NewUser(user_name=user, email=email, password=password).save()
        else:
            messages.error(request, "Password donot match.")
        return redirect('/login')

class LoginRequest(View):
    def get(self, request):
        return render(request, "user/login.html", context={})

    def post(self, request):
        username = request.POST.get('user')
        password = request.POST.get('pass')
        # def authenticate(self, request, username= None, password=None):
        #     try:
        #         # Try to find a user matching your username
        #         user = NewUser.objects.get(user_name=username)

        #         #  Check the password is the reverse of the username
        #         if check_password(password, user.password):
        #             # Yes? return the Django user object
        #             return user
        #         else:
        #             # No? return None - triggers default login failed
        #             return None
        #     except NewUser.DoesNotExist:
        #         # No user was found, return None - triggers default login failed
        #         return None

        # # Required for your backend to work properly - unchanged in most scenarios
        # def get_user(self, id):
        #     try:
        #         return NewUser.objects.get(pk=id)
        #     except NewUser.DoesNotExist:
        #         return None
        from user.backends import CaseInsensetiveModelBackend
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            messages.success(request, "You Have Been Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "username or password not match", extra_tags='alert')
            return redirect('/login')
        
            

class Logout(View):
    def get(self, request):
        try:
            del request.session['user_id']
        except:
            return redirect('/login')
        messages.error(request, "You Have Been Successfully Logged Out")
        return redirect('/login')








# match_user = User.objects.filter(username=username).first()
# user_password = match_user.check_password(password)
# if user_password is True: