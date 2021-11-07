from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from authUser.managers import CustomUserManager
import copy


class CustomAccount(AbstractUser):
    username = None
    email = None
    first_name = None
    last_name = None
    email_address = models.EmailField(max_length=50, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = []
