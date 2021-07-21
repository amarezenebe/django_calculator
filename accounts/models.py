from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class MyUserQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def featured(self):
        return self.filter(featured=True, active=True)


def firstName(value):
    if len(value) < 2 or len(value) > 20:
        raise ValidationError(
            "Should be 2-20 character.",
        )
    elif not value.isalpha():
        raise ValidationError(
            "Should be alphabets.",

        )


def nickName(value):
    if len(value) < 5 or len(value) > 20:
        raise ValidationError(
            "You Nick name should be 5-20 character.",
        )


def lastName(value):
    if len(value) < 2 or len(value) > 20:
        raise ValidationError(
            "Should be 2-20 character.",
        )
    elif not value.isalpha():
        raise ValidationError(
            "Should be alphabets.",
        )


class MyUserManager(BaseUserManager):
    def get_queryset(self):
        return MyUserQuerySet(self.model, using=self._db)

    def create_user(self, nick, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user=self.model(
            nick=nick,
            first_name=first_name,
            last_name=last_name,
            is_admin=True,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nick, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user=self.create_user(
            nick=nick,
            first_name=first_name,
            last_name=last_name,
            password=password,

        )
        return user

    def active(self):
        return self.filter(is_active=True)


class User(AbstractBaseUser):
    nick=models.CharField(max_length=255, unique=True, validators=[nickName])
    first_name=models.CharField(max_length=255, validators=[firstName])
    last_name=models.CharField(max_length=255, validators=[lastName])
    is_active=models.BooleanField(default=True)  # can login
    is_staff=models.BooleanField(default=False)  # staff user non superuser
    is_admin=models.BooleanField(default=False)  # superuser
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    objects=MyUserManager()

    USERNAME_FIELD='nick'  # username
    REQUIRED_FIELDS=["first_name", "last_name", ]

    def __str__(self):
        return "{}{}".format(self.first_name, self.last_name)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name).title()

    @staticmethod
    def has_perm(perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# Create your models here.
class calculatorHistory(models.Model):
    input=models.CharField(max_length=250)
    result=models.CharField(max_length=250)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        return self.input

    def delete_history(self):
        return reverse("accounts:delete_history", kwargs={"id": self.id})
