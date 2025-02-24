#django files
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email, phone=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, phone, password):
        user = self.create_user(email, phone, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user





