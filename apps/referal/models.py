from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from abstract_models import AbstractModel


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        user = self.model(**kwargs)
        user.set_invite_code()
        user.save()
        return user

    def create_superuser(self, **kwargs):
        user = self.model(**kwargs)
        user.set_password(kwargs["password"])
        user.is_staff = True
        user.is_superuser = True
        user.set_invite_code()
        user.save()


class User(AbstractBaseUser, AbstractModel, PermissionsMixin):
    phone_number = models.CharField(_("Phone number"), unique=True)
    invite_code = models.CharField(
        _("Invite_code"),
        unique=True,
        blank=False,
        help_text='Code that other users can write to "refered_by" field',
    )
    login_code = models.CharField(
        _("Login code"),
        null=True,
        blank=True,
        help_text="Code that app send on phone number of user",
    )
    is_staff = models.BooleanField(
        _("Is staff"),
        default=False,
        help_text="Defines permission to login to admin site",
    )
    is_superuser = models.BooleanField(
        _("Is superuser"),
        default=False,
        help_text="Is user can login to admin site with all permissions",
    )
    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        indexes = [
            models.Index(fields=["id", "phone_number"]),
        ]

    def __str__(self) -> str:
        return self.phone_number

    def __repr__(self) -> str:
        return self.phone_number

    def set_invite_code(self):
        chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        invite_code = get_random_string(length=6, allowed_chars=chars)
        self.invite_code = invite_code
        self.save()

    def set_login_code(self):
        chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        login_code = get_random_string(length=4, allowed_chars=chars)
        self.login_code = login_code
        self.save()


class UserProfile(AbstractModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    refered_by = models.CharField(
        _("Refered by"), blank=True, help_text="Invite code of other user"
    )

    def __str__(self) -> str:
        return self.user.phone_number
