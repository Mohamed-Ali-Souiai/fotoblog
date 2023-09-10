from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
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
    blogs = models.Blog.objects.all()
    photos = models.Photo.objects.all()
    context = {'photos': photos, 'blogs': blogs}
    return render(request, 'blog/home.html', context=context)


class CreateMultiplePhotos(LoginRequiredMixin, View):
    PhotoFormset = formset_factory(forms.PhotoForm, extra=3)
    formset_class = PhotoFormset
    template_name = 'blog/create_multiple_photos.html'

    def get(self, request):
        formset = self.formset_class()
        context = {'formset': formset}
        return render(request, self.template_name, context=context)

    def post(self, request):
        formset = self.formset_class(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
        context = {'formset': formset}
        return render(request, self.template_name, context=context)


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
            blog.save()
            return redirect('home')
        context = {
            'form_blog': form_blog,
            'form_photo': form_photo
        }
        return render(request, self.template_name, context=context)


class EditBlog(LoginRequiredMixin, View):

    edit_form_class = forms.BlogForm
    delete_form_class = forms.DeleteBlogForm
    template_name = 'blog/edit_blog.html'

    def get(self, request, blog_id):
        blog = get_object_or_404(models.Blog, id=blog_id)
        edit_form = self.edit_form_class(instance=blog)
        delete_form = self.delete_form_class()
        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, blog_id):
        blog = get_object_or_404(models.Blog, id=blog_id)
        if 'edit_blog' in request.POST:
            edit_form = self.edit_form_class(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_blog' in request.POST:
            delete_form = self.delete_form_class(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')
        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
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
