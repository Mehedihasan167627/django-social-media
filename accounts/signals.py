from django.dispatch import receiver
from .models import CustomUser, Profile
from django.db.models.signals import post_save 
import random
from django.utils.text import slugify



@receiver(post_save,sender=CustomUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
        url=str(instance.username).replace("-","").replace("_","")
        while Profile.objects.filter(url=url).exists():
            url=url+str(random.randint(10,99)+Profile.objects.all().count())             
        Profile.objects.create(author=instance,url=slugify(url))
