from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout_view/', logout_view, name='logout_view'),
    path('register/', register, name='register'),
    path('register_button/', register_button, name='register_button'),
    path('change_password/', change_password, name='change_password'),
    path('api/v1/', include('applications.api.urls')),
    path('ubicaciones/', include('applications.ubicaciones.urls')),
    path('establecimientos/', include('applications.establecimientos.urls')),
]
