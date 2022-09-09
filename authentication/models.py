from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager

from api.models import ModelTemplate


class User(AbstractBaseUser, PermissionsMixin, ModelTemplate):
    """
    Custom User Model
    """

    phone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=50)

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'


