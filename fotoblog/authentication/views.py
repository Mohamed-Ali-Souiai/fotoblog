from django.shortcuts import render, redirect
from django.conf import settings
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class UploadProfilePhoto(View):
    form_class = forms.UploadProfilePhotoForm
    template_name = 'authentication/upload_profile_photo.html'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


class SignupPage(View):
    form_class = forms.SignupForm
    template_name = 'authentication/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, context={'form': form})


class LoginPageView(View,LoginRequiredMixin):
    form_class = forms.LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(
            request,
            self.template_name,
            context={'message': message, 'form': form}
        )

    def post(self, request):
        message = ''
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
                # message = f'Bonjour, {user.username}! vous êtes connecté.'
            else:
                message = 'identifiant invalide.'
        return render(
            request,
            self.template_name,
            context={'message': message, 'form': form}
        )


def logout_user(request):
    logout(request)
    return redirect('login_page')


"""def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
                # message = f'Bonjour, {user.username}! vous êtes connecté.'
            else:
                message = 'identifiant invalide.'
    return render(
        request,
        'authentication/login.html',
        context={'message': message, 'form': form}
    )"""
