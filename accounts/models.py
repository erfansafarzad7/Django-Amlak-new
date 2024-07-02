from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from .managers import UserManager
import random


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_otp')
    code = models.CharField(max_length=5, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.code}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        random_code = random.randint(10000, 99999)
        OTP.objects.create(user=instance, code=random_code)

        if instance.email:
            send_mail(
                "Your OTP Code :",
                f"Hi There . There Is Your Code : {random_code}",
                "efi.dragon20002gmail.com",
                [instance.email, ]
            )
            print(random_code)
