from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/<int:room_id>', views.room, name='room'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/', views.register, name='register'),
    path('create-booking/<int:room_id>', views.create_booking, name='booking_form'),
    path('rooms/economy/', views.economy, name='economy'),
    path('rooms/comfort/', views.comfort, name='comfort'),
    path('rooms/business/', views.business, name='business'),
    path('rooms/premium/', views.premium, name='premium'),
    path('booking/delete/<int:booking_id>', views.delete_booking, name='delete_booking'),
    path('rooms/search/', views.search_results, name='search_results')
]
