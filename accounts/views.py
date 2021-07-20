from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    logout_then_login
)
from django.shortcuts import redirect, reverse, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView, ListView

from accounts.forms import RegistrationForm, Calculator, ChangeProfileForm, SignInForm
# Good 1
from accounts.models import calculatorHistory


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class SignUpView(GuestOnlyView, FormView):
    template_name='accounts/sign_up.html'
    form_class=RegistrationForm

    def form_valid(self, form):
        # collect the user information
        user=form.save(commit=False)
        password=form.cleaned_data.get("password1")
        user.set_password(password)
        user.save()
        messages.success(self.request, _(' successfully Sin up .'))

        return redirect(reverse("accounts:login"))


# Good 5
class LogInView(GuestOnlyView, FormView):
    template_name='accounts/login.html'
    form_class=SignInForm

    def get_initial(self):
        initial=super().get_initial()
        initial['request']=self.request
        return initial

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    # @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request=self.request
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        login(request, form.user_cache)
        messages.success(self.request, _(f'welcome {self.request.user.full_name()}.'))

        return redirect(reverse("accounts:home"))


class LogOutView(LoginRequiredMixin, View):
    def post(self, request):
        messages.success(self.request, _(' successfully Log out.'))

        logout_then_login(request)
        return redirect(reverse("accounts:login"))


class Home(LoginRequiredMixin, FormView):
    template_name='accounts/home.html'
    form_class=Calculator

    def form_valid(self, form):
        user_input=form.cleaned_data.get("input")
        try:
            result=eval(user_input)

        except Exception as e:
            if str(e).find("(<string>, line 1)") > -1:
                result='Is not correct Mathematical input'
            else:
                # in order to use some math syntax like 1>0 ,2*(2+43)>5
                result=str(e)
        calculatorHistory.objects.create(
            user=self.request.user,
            input=user_input,
            result=result

        )
        return render(self.request, "accounts/home.html", {
            "form": Calculator(initial={"input": user_input, "result": result})
        })


class userHistory(LoginRequiredMixin, ListView):
    template_name='accounts/userHistory.html'

    # specify the model for list view
    model=calculatorHistory

    def get_queryset(self, *args, **kwargs):
        qs=super(userHistory, self).get_queryset(*args, **kwargs)
        qs=qs.filter(user=self.request.user).order_by("-id")
        return qs


@login_required
def ProfileView(request):
    template_name='accounts/your_profile.html'
    return render(request, template_name)


@login_required
def deleteHistory(request, id):
    history=calculatorHistory.objects.filter(user=request.user, id=id)
    if history.exists():
        history.delete()
        messages.success(request, _('History  has been successfully Deleted.'))
    else:
        messages.success(request, _('Sorry this history is not exist'))

    return redirect(reverse("accounts:history"))


@login_required
def deleteAllHistory(request, ):
    history=calculatorHistory.objects.filter(user=request.user)
    if history.exists():
        history.delete()
        messages.success(request, _('All History  has been successfully Deleted.'))
    else:
        messages.warning(request, _('Sorry there is  history to delete'))
    return redirect(reverse("accounts:history"))


class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name='accounts/change_profile.html'
    form_class=ChangeProfileForm

    def get_form_kwargs(self):
        kwargs=super(ChangeProfileView, self).get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        kwargs.update({'initial': {"password": ""}})
        return kwargs

    def form_valid(self, form):
        user=form.save(commit=False)
        password=form.cleaned_data.get("password", None)
        if password is not None:
            user.set_password(password)
            update_session_auth_hash(self.request, user)
        user.save()
        messages.warning(self.request, _('Profile  has been successfully updated.'))

        return redirect('accounts:profile')
