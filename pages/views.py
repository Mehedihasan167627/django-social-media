
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views import View

from accounts.forms import ProfileEditForm
from accounts.models import CustomUser, Profile 
from django.contrib import messages
from django.conf import settings

from posts.forms import PostAddForm
from posts.models import Comment, Post
from .helpers import DummyUserThead

class HomeView(View):
    def get(self,request):
        profile=Profile.objects.get(author=request.user)
        following_id=[profile.id] 
        for p in profile.following.all():
            following_id.append(p.id)


        posts=Post.objects.filter(author_id__in=following_id).order_by("-created_at")
        profile_list=Profile.objects.exclude(id__in=following_id)[:10]

        context={
            "posts":posts,
            "profile_list":profile_list
           
        }
        return render(request,"pages/index.html",context)




class FriendProfileView(View):
    def get(self,request,url):
        try:
            profile=Profile.objects.get(url=url)
            if profile==Profile.objects.get(author=request.user):
                return redirect("pages:profile")
        except:
            return HttpResponse("invalid url")

        

        context={
            "profile":profile
        }
        return render(request,"pages/friend-profile.html",context)



class ProfileView(View):
    def get(self,request):
        profile=Profile.objects.get(author=request.user)
        return render(request,"pages/profile.html",{"profile":profile})


class ProfileEditView(View):
    def get(self,request):
        author=Profile.objects.get(author=request.user)
        form=ProfileEditForm(instance=author)

        return render(request,"pages/edit-profile.html",{"form":form,"media_url":settings.MEDIA_URL})      
    def post(self,request):
        author=Profile.objects.get(author=request.user)
        form=ProfileEditForm(request.POST or None, request.FILES,instance=author)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Profile Updated!!")
        return render(request,"pages/edit-profile.html",{"form":form})
        

class PostAddView(View):
    def get(self,request):
        form=PostAddForm()
        return render(request,"posts/add.html",{"form":form})

    def post(self,request):
        author=Profile.objects.get(author=request.user)
        form=PostAddForm(request.POST or None, request.FILES)
  
        if form.is_valid():
            post=form.save(commit=False) 
            post.author=author
            post.save()
            messages.success(request,"Post created successfully!!")
            return redirect("pages:home")
        return render(request,"posts/add.html")




class FollowUnfollowView(View):
    def post(self,request):
        url=request.POST.get("url")
        msg=""
        count=0
        if Profile.objects.filter(url=url).exists():
            receiver=Profile.objects.get(url=url)
            sender=Profile.objects.get(author=request.user)
            
            msg,count=Profile.add_or_remove(sender,receiver)
            
        return JsonResponse({"message":msg,"count":count,"status":200})

class LikeUnlikeView(View):
    def post(self,request):
        slug=request.POST.get("post_slug")
        if Post.objects.filter(slug=slug).exists():
            post=Post.objects.get(slug=slug)
            sender=Profile.objects.get(author=request.user)  
            msg,count=Post.add_or_remove(sender,post)
            
        return JsonResponse({"message":msg,"count":count,"status":200})


class PostCommentView(View):
    def post(self,request):
        post_url=request.POST.get("post_id")
        comment=request.POST.get("comment")
        if Post.objects.filter(slug=post_url).exists():
            post=Post.objects.get(slug=post_url)
            sender=Profile.objects.get(author=request.user)
            obj=Comment.objects.create(post=post,body=comment,comment_by=sender)
            count=Comment.objects.filter(post=post).count()
            comment_list={
                      "comment":obj.body,
                      "post_url":obj.post.slug,
                      "creator":obj.comment_by.url,
                      "creator_profile":obj.comment_by.avatar.url ,
                      "time":obj.created,
                      "comment_count":count,
                      }
        return JsonResponse({"result":comment_list,})



class  FindFriendView(View):
    def get(self,request):
        
        profile=Profile.objects.get(author=request.user)
        following_id=[profile.id] 
        for p in profile.following.all():
            following_id.append(p.id)
        profile_list=Profile.objects.exclude(id__in=following_id)[:50]

        context={
            "profile_list":profile_list
           
        }
        return render(request,"pages/find-friend.html",context)