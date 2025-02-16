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
from django.urls import path, reverse, re_path# type: ignore
from reservas import views # type: ignore
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import register, profile, superadmin_required, CustomLoginView

from users.views import CustomLoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='login'),
    path('index/', views.index),

    path('Configuracion/', views.config, name='config'), 
    path('Sobre/', views.about,  name='about'),
      
    path('Balsas/', views.balsas,  name='balsas'),
    path('Balsa/', views.nueva_balsa, name='balsa'),
    path('Balsa/editar/<int:balsa_id>/', views.editar_balsa, name='editar_balsa'),
    path('balsas/eliminar/<int:balsa_id>/', views.eliminar_balsa, name='eliminar_balsa'),

    path('Bajadas/', views.bajadas,  name='bajadas'),
    path('Bajada_nueva/', views.nueva_bajada,  name='nueva_bajada'),
    path('Bajada/<int:bajada_id>', views.editar_bajada,  name='editar_bajada'),

    path('obtener_bajadas_json/', views.obtener_bajadas_json,  name='obtener_bajadas_json'),


    


    path('Usuario_nuevo/', views.nuevo_navegante, name='nuevocliente'),
    path('Usuario/<str:documento>/editar/', views.editar_navegante, name='editar_usuario'),
    path('Usuario/<str:documento>/eliminar/', views.eliminar_navegante, name='eliminar_navegante'),
    path('Navegantes/', views.navegantes, name='navegantes'),

    path('Recorridos/', views.recorridos,  name='recorridos'),
    path('Recorrido_nuevo/', views.nuevo_recorrido,  name='recorrido_nuevo'),
    path('Recorrido/<int:recorrido_id>', views.editar_recorrido,  name='editar_recorrido'),
    path('eliminar/<int:pk>/', views.eliminar_recorrido, name='eliminar_recorrido'),

    # path('registro/', register, name='registro'),
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('Usuario/', views.profile, name='pro_file'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', superadmin_required(profile), name='profile') 
    
]




