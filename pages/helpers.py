from accounts.models import CustomUser
from faker import Faker
import random 
from django.contrib.auth.hashers import make_password
fake=Faker() 
import threading

class DummyUserThead(threading.Thread):
    def __init__(self,total):
        self.total=total 
        threading.Thread.__init__(self) 


    def run(self):
        for i in range(self.total):
            email=fake.email()
            while CustomUser.objects.filter(email=email).exists():
                email=fake.email()
            CustomUser.objects.create(
                username=str(fake.name()).replace(" ","_").lower(),
                    email=email,
                    password=make_password("123"),
                    verification_code=random.randint(10000,99999),
                    is_active=True 
            )
        return "Done"






