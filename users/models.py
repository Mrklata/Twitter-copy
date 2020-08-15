from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password=None, is_staff=False, is_admin=False, is_active=False):
        if not email and username:
            raise ValueError("Users must have username and email")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(unique=True, max_length=20)
    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)  # superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return f'name: {self.first_name}, surname: {self.last_name}'

    def get_short_name(self):
        return self.first_name

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmed_account = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
