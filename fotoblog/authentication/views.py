from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login, logout


def login_page(request):
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
    )


def logout_user(request):
    logout(request)
    return redirect('login_page')
