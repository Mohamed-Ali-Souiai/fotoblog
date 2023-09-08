from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login_page'),
    path('logout', authentication.views.logout_user, name='logout'),
    path('signup', authentication.views.SignupPage.as_view(), name='signup'),
    path('home', blog.views.home, name='home'),
    path('photo/upload/', blog.views.PhotoUpload.as_view(), name='photo_upload'),
    path('profile-photo/upload', authentication.views.UploadProfilePhoto.as_view(),
         name='upload_profile_photo'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""