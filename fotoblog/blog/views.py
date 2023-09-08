from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models


@login_required
def home(request):
    photos = models.Photo.objects.all()
    return render(request, 'blog/home.html', {'photos': photos})


class PhotoUpload(LoginRequiredMixin, View):
    form_class = forms.PhotoForm
    template_name = 'blog/photo_upload.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})
