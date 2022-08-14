
from django.contrib.auth.base_user import BaseUserManager
import random

class UserModel(BaseUserManager):
    user_in_migrations=True 

    def create_user(self,email,password=None,**kwargs):
        if not email:
            raise ValueError("Email Field is required")
        
        email=self.normalize_email(email) 
        user=self.model(email=email,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self,email,password,**kwargs):
        kwargs.setdefault("is_superuser",True)
        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_active",True)
        kwargs.setdefault("verify",True)
        kwargs.setdefault("verification_code",random.randint(10000,99999))

        if kwargs.get("is_staff") is not True:
            raise ValueError(('Super user must have Staff user'))

        return self.create_user(email,password,**kwargs)
