from django.contrib import admin

from django.contrib import admin
import blog.models
# Register your models here.


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'caption', 'id')


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')


admin.site.register(blog.models.Photo, PhotoAdmin)
admin.site.register(blog.models.Blog, BlogAdmin)
