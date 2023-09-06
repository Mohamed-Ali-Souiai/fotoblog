from django.shortcuts import render
from . import forms
from django.contrib.auth import authenticate, login


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['passwoed']
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! vous êtes connecté.'
            else:
                message = 'identifiant invalide.'
    return render(
        request,
        'authentcation/login.html',
        context={'message': message, 'form': form}
    )
