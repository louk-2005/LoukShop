#django files
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

#your files
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone = models.CharField(max_length=11, null=True, blank=True)
    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return f'{self.email}'

class ResetPassword(models.Model):
    email = models.EmailField()
    token = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.token}'







