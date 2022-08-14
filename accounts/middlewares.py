from django.contrib import messages
from django.shortcuts import redirect
from .models import Profile

def auth_middleware(get_response):
    def middleware(request):
        return_url=request.META["PATH_INFO"]   
        
        if request.user.is_authenticated==False:
            messages.warning(request,"Please Login with your account")
            return redirect(f"/accounts/login/?return_url={return_url}")
   

        response=get_response(request)
        return response

    return middleware

def auth_middleware_w_slug(get_response):
    def middleware(request,url=None):
        return_url=request.META["PATH_INFO"]   
        print(return_url) 
        if request.user.is_authenticated==False:
            messages.warning(request,"Please Login with your account")
            return redirect(f"/accounts/login/?return_url={return_url}")
   
        response=get_response(request,url)
        return response

    return middleware


