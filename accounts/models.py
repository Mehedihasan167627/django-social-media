
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserModel




class CustomUser(AbstractUser):
    username=models.CharField(max_length=100,blank=True,null=True) 
    email=models.EmailField(unique=True)
    verification_code=models.CharField(max_length=5,blank=True,null=True)
    verify=models.BooleanField(default=False)
    objects=UserModel()
    
    USERNAME_FIELD='email'

    REQUIRED_FIELDS=[]


class Profile(models.Model):
    author=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100,blank=True,null=True)
    last_name=models.CharField(max_length=100,blank=True,null=True)
    location=models.CharField(max_length=100,blank=True,null=True)
    url=models.CharField(max_length=50,blank=True,null=True)
    avatar=models.ImageField(upload_to="accounts/uploads/profile",default="accounts/uploads/default-user.png")
    profile_info=models.TextField(blank=True,null=True)
    follower=models.ManyToManyField(CustomUser,related_name="follower",blank=True) 
    following=models.ManyToManyField(CustomUser,related_name="following",blank=True) 
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.author.email 
    

    def my_followers(self):
        return self.followers.all()
    def i_follow(self):
        return self.followings.all()

    @staticmethod
    def add_or_remove(sender,receiver):
        sender_=CustomUser.objects.get(email=sender)
        receiver_=CustomUser.objects.get(email=receiver)
        msg=""
        if sender_ in receiver.follower.all():
            receiver.follower.remove(sender_)
            sender.following.remove(receiver_)
            msg="remove"
        else:       
            receiver.follower.add(sender_)
            sender.following.add(receiver_)
            msg="add"
        count=receiver.follower.all().count()
        return msg ,count




