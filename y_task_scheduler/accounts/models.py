from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import datetime

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("The Login field must be set")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    login = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    register_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['login']

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    def set_password(self, input_password):
        self.password = make_password(input_password)

    def check_password(self, input_password):
        return check_password(input_password, self.password)
    
    def normalize_all(self):
        self.name = self.name.capitalize()
        self.last_name = self.last_name.capitalize()

    def __str__(self):
        return f"{self.name} {self.last_name}"
    