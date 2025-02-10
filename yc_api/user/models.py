from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Create and return a regular user with an username and password.
        """
        if not username:
            raise ValueError('The Username field must be set')
        
        extra_fields.setdefault('is_active', True)  # Set is_active to False for regular users
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser with an username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Set is_active to True for superusers

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True)
    is_active = models.BooleanField(default=True)  # Default is_active to False
    top_streak = models.IntegerField(default=0, blank=True, null=True)
    current_streak = models.IntegerField(default=0, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    last_study_date = models.DateField(null=True, blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    total_study_hours = models.IntegerField(default=0)
    # last_start_study_date = models.DateField(auto_now=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} {self.last_name} - {self.username}"
        return self.username
