from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login_page'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('logout', authentication.views.logout_user, name='logout'),
    path('signup', authentication.views.SignupPage.as_view(), name='signup'),
    path('home', blog.views.home, name='home'),
    path('photo/upload/', blog.views.PhotoUpload.as_view(), name='photo_upload'),
    path('profile-photo/upload', authentication.views.UploadProfilePhoto.as_view(),
         name='upload_profile_photo'),
    path('blog/create/', blog.views.BlogAndPhotoUpload.as_view(), name='create_blog'),
    path('blog/<int:blog_id>', blog.views.view_blog, name='view_blog'),
    path('blog/<int:blog_id>/edit', blog.views.EditBlog.as_view(), name='edit_blog'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""