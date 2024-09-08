from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=255, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = 'Restaurant'
    
    def __str__(self):
        return self.name
    
class Menu(models.Model):

    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    day_of_week = models.CharField(choices=DAYS_OF_WEEK)
    items = models.JSONField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('restaurant', 'day_of_week')
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
    
    def __str__(self):
        return f"Menu for {self.restaurant.name} on {self.days_of_week}"
    
from django.conf import settings

class Vote(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_id = models.ForeignKey('Menu', on_delete=models.CASCADE)
    vote_time = models.DateTimeField(default=timezone.now)


    # class Meta:
    #     unique_together = ('user_id', 'menu_id')

    def __str__(self):
        return f"{self.employee.username} voted for {self.menu.restaurant.name} on {self.menu.date}"