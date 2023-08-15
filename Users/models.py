from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import *

# Create your models here.


class UserInfo(AbstractBaseUser, PermissionsMixin):
    created_by = models.URLField(max_length=200,null=True,blank=True)
    updated_by = models.URLField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    firstname = models.CharField(max_length=50, verbose_name="First Name")
    lastname = models.CharField(max_length=50, verbose_name="Second Name")
    password = models.CharField(max_length=50, verbose_name="Password")
    email = models.EmailField(verbose_name="Email", unique=True)
    phone = models.CharField(max_length=11, verbose_name="Phone Number")                  #need to change to be unique
    is_staff = models.BooleanField(default=False)
    is_Active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomManager()

    def __str__(self):
        return self.firstname
