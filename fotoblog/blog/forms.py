from . import models
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'caption']


class BlogForm(forms.ModelForm):
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Blog
        fields = ['title', 'content']


"""Ces champs utilisent le widget   HiddenInput   ,
et ne seront pas vus par l’utilisateur sur le front-end.
Le choix du type de champ et de la valeur initiale est quelque peu arbitraire,
vu que nous allons simplement vérifier la présence du champ dans la vue."""


class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
