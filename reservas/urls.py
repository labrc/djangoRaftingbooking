from django.urls import path, reverse, re_path# type: ignore
from . import views # type: ignore
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import register, profile, superadmin_required, CustomLoginView

from users.views import CustomLoginView


urlpatterns = [
    path('', views.index, name='index'),


    path('Configuracion/', views.config, name='config'), 
    path('Sobre/', views.about,  name='about'),
    path('acceso/', views.acceso,  name='no_access'),
      
    path('Balsas/', views.balsas,  name='balsas'),
    path('Balsa/', views.nueva_balsa, name='balsa'),
    path('Balsa/editar/<int:balsa_id>/', views.editar_balsa, name='editar_balsa'),
    path('balsas/eliminar/<int:balsa_id>/', views.eliminar_balsa, name='eliminar_balsa'),

    path('exportar_planilla/<int:bajada_id>/', views.exportar_planilla, name='exportar_planilla'),

    path('Bajadas/', views.lista_bajadas,  name='bajadas'),
    path('Bajada_nueva/', views.nueva_bajada,  name='nueva_bajada'),
    path('Bajada/<int:bajada_id>', views.editar_bajada,  name='editar_bajada'),
    path('bajada/borrar/<int:bajada_id>/', views.borrar_bajada, name='borrar_bajada'),

    path('obtener_bajadas_json/', views.obtener_bajadas_json,  name='obtener_bajadas_json'),

    

    path("agregar_csv/", views.agregar_por_csv, name="agregar_por_csv"),
    path("procesar_csv/", views.procesar_csv, name="procesar_csv"),



    path('Usuario_nuevo/', views.nuevo_navegante, name='nuevocliente'),
    path('Usuario/<str:documento>/editar/', views.editar_navegante, name='editar_usuario'),
    path('Usuario/<str:documento>/eliminar/', views.eliminar_navegante, name='eliminar_navegante'),
    path('Navegantes/', views.navegantes, name='navegantes'),

    path('Recorridos/', views.recorridos,  name='recorridos'),
    path('Recorrido_nuevo/', views.nuevo_recorrido,  name='recorrido_nuevo'),
    path('Recorrido/<int:recorrido_id>', views.editar_recorrido,  name='editar_recorrido'),
    path('eliminar/<int:pk>/', views.eliminar_recorrido, name='eliminar_recorrido'),

    
]




