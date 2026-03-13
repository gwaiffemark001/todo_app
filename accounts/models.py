from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    username=models.CharField(max_length=150, unique=True)
    phone=models.CharField(max_length=11)
    profile_picture=models.ImageField(upload_to='profiles/')
    bio=models.TextField(max_length=500)
    def __str__(self):
        return self.username
    