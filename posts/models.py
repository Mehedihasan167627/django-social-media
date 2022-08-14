
import random
from django.db import models
from accounts.models import Profile 
from django.utils.text import slugify

class Post(models.Model):
    author=models.ForeignKey(Profile,on_delete=models.CASCADE)
    caption=models.TextField()
    thumbnail=models.ImageField(upload_to="posts/uploads",blank=True,null=True,verbose_name="Image")
    likes=models.ManyToManyField(Profile,related_name="links",blank=True)
    slug=models.SlugField(blank=True,null=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.caption 


    def check_slug(self,cap):
        slug=str(cap).replace(" ","")
        if len(slug)>10:slug=str(slug)[:10] 
         
        slug=slugify(slug)
        while Post.objects.filter(slug=slug).exists():
            slug=slug+str(random.randint(100000,999999))
        return slug

    

    def save(self,*args,**kwargs):
        if not self.slug:
           slug=self.check_slug(self.caption)
           self.slug=slug 
        return super().save(*args,**kwargs)

    
    @staticmethod
    def add_or_remove(sender,post):
        
        msg=""
        if sender in post.likes.all():
            post.likes.remove(sender)
            msg="remove"
        else:       
            post.likes.add(sender)
            msg="add"

        count=post.likes.count()

        return msg ,count


class PostImage(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE) 
    image=models.ImageField(upload_to="posts/uploads")

    def __str__(self) -> str:
        return self.post.caption 


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_by=models.ForeignKey(Profile,on_delete=models.CASCADE)
    body=models.TextField(max_length=240)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
