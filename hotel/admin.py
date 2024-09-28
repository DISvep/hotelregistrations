from django.contrib import admin
from .models import User, Floor, Room, Booking


# Register your models here.
admin.site.register(User)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Booking)
