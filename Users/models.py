from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(unique=True, max_length=13)
    nationality_id = models.CharField(unique=True, max_length=10)
    occupation = models.CharField(max_length=100)
    salary = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nationality_id', 'phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
