from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('floor/<int:floor_id>', views.floor, name='floor'),
    path('room/<int:room_id>', views.room, name='room'),
    path('booking/', views.booking, name='booking'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/', views.register, name='register'),
    path('create-booking/', views.create_booking, name='booking_form')
]
