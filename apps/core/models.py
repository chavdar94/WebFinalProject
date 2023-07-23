from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from django.utils import timezone
from django.shortcuts import reverse

from .managers import AppUserManager
from .validators import validate_file_size


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    objects = AppUserManager()

    def __str__(self):
        name_from_email = self.email.split('@')[0]
        return name_from_email

    @property
    def user_name(self):
        name_from_email = self.email.split('@')[0]
        return name_from_email

    class Meta:
        ordering = ['pk']


UserModel = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    age = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    city = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    profile_picture = models.FileField(
        upload_to='profile-pictures',
        null=True,
        blank=True,
        validators=(validate_file_size,),
    )

    objects = models.Manager()

    @property
    def get_full_name(self):
        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

    def get_absolute_url(self):
        return reverse("profile-page", kwargs={"pk": self.pk})

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.user.email
