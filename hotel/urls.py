from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('floor/<int:floor_id>', views.floor, name='floor'),
    path('room/<int:room_id>', views.room, name='room'),
    path('booking', views.booking, name='booking')
]
