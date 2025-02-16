"""
URL configuration for sitio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path, reverse, re_path, include# type: ignore
from reservas import views # type: ignore
from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import register, profile, superadmin_required, CustomLoginView

from users.views import CustomLoginView
from django.conf.urls import handler400, handler403, handler404, handler500


handler400 = "reservas.views.error_400"
handler403 = "reservas.views.error_403"
handler404 = "reservas.views.error_404"
handler500 = "reservas.views.error_500"
handler503 = "reservas.views.error_503"


urlpatterns = [
    path('admin/', admin.site.urls, name='adminpage'),
    path('', include('reservas.urls'), name='start'),
    path('usuarios/', include('users.urls') ),
    path('usuarios/', include('django.contrib.auth.urls') ),

]




