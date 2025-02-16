from django.urls import path, reverse, re_path# type: ignore
from . import views # type: ignore


urlpatterns = [


    #path('login/', CustomLoginView.as_view(), name='login'),
    path('login/', views.login_user, name='login'),
    path('', views.login_user, ),
    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', views.logout_user, name='logout'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile') 
    
]




