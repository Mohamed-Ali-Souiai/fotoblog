from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models


@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})


@login_required
def home(request):
    photos = models.Photo.objects.all()
    blogs = models.Blog.objects.all()
    context = {'photos': photos, 'blogs': blogs}
    return render(request, 'blog/home.html', context=context)


class BlogAndPhotoUpload(LoginRequiredMixin, View):
    form_blog_class = forms.BlogForm
    form_photo_class = forms.PhotoForm
    template_name = 'blog/create_blog_post.html'

    def get(self, request):
        form_blog = self.form_blog_class()
        form_photo = self.form_photo_class()
        context = {
            'form_blog': form_blog,
            'form_photo': form_photo
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form_blog = self.form_blog_class(request.POST)
        form_photo = self.form_photo_class(request.POST, request.FILES)
        if all([form_blog.is_valid(), form_photo.is_valid]):
            photo = form_photo.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = form_blog.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            return redirect('home')
        context = {
            'form_blog': form_blog,
            'form_photo': form_photo
        }
        return render(request, self.template_name, context=context)


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
