from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
import uuid

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """ user model
    """
    email = models.EmailField(max_length=500, unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    handle = models.CharField(max_length=150)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.handle = self.trimmed_email

        return super(User, self).save(*args, **kwargs)

    def get_short_name(self):
        return f"{self.first_name}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".title()

    @property
    def get_display_name(self):
        if self.first_name and self.last_name:
            return self.get_full_name
        return f"{self.email}"

    @property
    def trimmed_email(self):
        return self.email.split("@")[0]

class Confirmation(models.Model):
    """ change password confirmation model
    """
    id = models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    url = models.CharField(max_length=500, default='')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        self.url = reverse('users:changepass', args={str(self.id)})

        return super(Confirmation, self).save(*args, **kwargs)
