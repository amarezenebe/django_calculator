from django import forms
from django.contrib.auth import password_validation
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCacheMixin:
    user_cache=None
    userType=None
    user_name=None


validators=RegexValidator("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
                          message="Minimum eight characters, at least one uppercase letter, "
                                  "one lowercase letter and one number:")


class RegistrationForm(forms.ModelForm):
    password1=forms.CharField(label=_('Password'), widget=forms.PasswordInput, validators=[validators])
    password2=forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput, validators=[validators])

    class Meta:
        model=User
        fields=("nick", 'first_name', "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        # Check that the two password entries match
        password1=self.cleaned_data.get("password1")
        password2=self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        password_validation.validate_password(password1)

        return password2


class LoginForm(forms.Form):
    email=forms.EmailField(label='Phone number or email ', )
    password=forms.CharField(widget=forms.PasswordInput)


class SignIn(UserCacheMixin, forms.Form):
    password=forms.CharField(label=_('Password'), strip=False,
                             widget=forms.PasswordInput()
                             )

    def clean_password(self):
        password=self.cleaned_data.get('password')
        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('You email or password invalid.'))

        return password


class SignInForm(SignIn):
    nick=forms.CharField(label=_('nick'), )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request=kwargs["initial"]["request"]

    @property
    def field_order(self):
        return ['nick', 'password', ]

    def clean_nick(self):
        nick=self.cleaned_data.get('nick')
        user=User.objects.filter(nick=nick).first()
        if not user:
            raise ValidationError(_('You email or password invalid.'))
        self.user_cache=user
        return nick


class ChangeProfileForm(forms.ModelForm):
    password=forms.CharField(label=_('Password'), widget=forms.PasswordInput, validators=[validators], required=False)

    class Meta:
        model=User
        fields=('first_name', "last_name", "password")


class Calculator(forms.Form):
    input=forms.CharField(max_length=250, label="Expiration")
    result=forms.CharField(max_length=250, required=False)
