from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import AbstractUser

from Review.models import *

CLIENT,FREELANCER=('client','freelancer')

class User(AbstractUser):
    ROLE_CHOICE=(
    ( CLIENT,'client'),
    ( FREELANCER,'freelancer')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.role}"

class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    username=models.CharField(max_length=25,unique=True)
    email = models.EmailField(unique=True)





