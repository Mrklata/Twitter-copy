from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.urls import reverse


class UserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password=None, staff=False, admin=False, active=True):
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
        user_obj.staff = staff
        user_obj.admin = admin
        user_obj.active = active
        user_obj.save(using=self._db)

        Profile.objects.create(
            user=user_obj
        )
        return user_obj

    def create_staffuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password=password,
            staff=True
        )
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password=password,
            staff=True,
            admin=True
        )
        return user


class User(AbstractBaseUser):
    objects = UserManager()
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    last_login = models.DateTimeField(auto_now_add=True)
    username = models.CharField(unique=True, max_length=20)
    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staffuser
    admin = models.BooleanField(default=False)  # superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

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


class FriendRequest(models.Model):
    STATUSES = (
        ('pending', 'pending'),
        ('declined', 'declined'),
        ('accepted', 'accepted')
    )

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')

    class Meta:
        verbose_name = 'Friend request'
        verbose_name_plural = 'Friend requests'
        unique_together = ['from_user', 'to_user']

    def __str__(self):
        return f'Request from {self.from_user}, to {self.to_user}'

    def get_absolute_url(self):
        pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmed_account = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    friends_list = models.ManyToManyField('Profile', blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        pass
