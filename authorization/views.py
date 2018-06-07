from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout


# Create your views here.
class RegisterFormView(FormView):

    form_class = UserCreationForm
    success_url = "login"
    template_name = "authorization/register.html"



    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class AuthForm(FormView):

    form_class = AuthenticationForm
    template_name = "authorization/login.html"
    success_url = "/"

    def get_form(self):
        form = super(AuthForm, self).get_form()
        form.fields['username'].label = "Имя пользователя"
        form.fields['password'].label = "Пароль"
        return form

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(AuthForm, self).form_valid(form)


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class BasicView(View):
    template_name = "base.html"
    def get(self, request):
        return render(request, self.template_name)
        