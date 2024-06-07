from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
Phone_Regex = RegexValidator( regex=r'^\d{10}$', message="Phone number must have 10 digits")


class CustomUserManager(BaseUserManager):
    def create_user(self, email_id, password=None, **extra_fields):
        if not email_id:
            raise ValueError("The Email field must be set")
        email_id = self.normalize_email(email_id)
        user = self.model(email_id=email_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email_id = models.EmailField(unique=True, max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"



from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)