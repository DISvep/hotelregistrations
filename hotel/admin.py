from django.contrib import admin
from .models import User, Floor, Room, Booking, Review

# Register your models here.
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)
