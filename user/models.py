# from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

about="Alias aperiam at debitis deserunt dignissimos dolorem doloribus, fuga fugiat impedit laudantium magni maxime nihil nisi quidem quisquam sed ullam voluptas voluptatum. Lorem ipsum dolor sit amet, consectetur adipisicing elit."

# Custom User model
class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(max_length=1, default='F')
    date_joined=models.DateTimeField(auto_now_add=True)
    about=models.TextField(default=about)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    complete=models.BooleanField(default=False)
    image=models.ImageField(upload_to="profile_Image",default="profile_image/concert.jpg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # this appears alongside the username in an object’s history
    #  in django.contrib.admin.
    def get_full_name(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize()

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

