
from django.contrib.auth import login,logout,authenticate
from django.views import View 
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import CustomUser
import random


class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect("pages:home")
        return render(request,'accounts/login.html')
    
    def check_email(self,email):
        return CustomUser.objects.filter(email=email)
 
    def post(self,request):
        email=request.POST.get("email")
        password=request.POST.get("password")
        if not self.check_email(email):
            messages.warning(request,"User not a user!!")
            return redirect("accounts:login")

        url_check=False 
        user=authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You're logged in successfully!!")
            return redirect("pages:home")    
        else:
            messages.warning(request,"Email or password is incorrect!!")
            return render(request,'accounts/login.html',{"email":email,"url_check":url_check})

class RegisterView(View):
    def get(self,request): 
        if request.user.is_authenticated:
            return redirect("pages:home")
        return render(request,"accounts/register.html")
    def post(self,request):
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        password=request.POST.get("password")
        email_check=CustomUser.objects.filter(email=email)

        if not email_check:
            user=CustomUser(
                username=str(username).replace(" ","_").lower(),
                email=email,
                password=make_password(password),
                verification_code=random.randint(10000,99999),
                is_active=True 
                )

            user.save()
            if user:
                messages.success(request,"Your account created successfully!!")
                return redirect("accounts:login")
        else:
            messages.warning(request,"Email address already exists!!!")
            return redirect("accounts:register")





class LogoutView(View):
    def get(self,request): 
        logout(request)
        messages.success(request,"You're logged out successfully!!")
        return redirect("accounts:login")


