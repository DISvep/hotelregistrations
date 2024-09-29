from django.shortcuts import render
from .models import Floor, Room, Booking


# Create your views here.
def index(request):
    floors = Floor.objects.all()
    rooms = Room.objects.all()

    context = {
        'floors': floors,
        'rooms': rooms
    }

    return render(
        request,
        'index.html',
        context=context
    )


def floor(request, floor_id):
    cur_floor = Floor.objects.filter(id=floor_id).first()

    context = {
        'floor': cur_floor
    }

    return render(
        request,
        'floor.html',
        context=context
    )


def room(request, room_id):
    cur_room = Room.objects.filter(id=room_id).first()

    context = {
        'room': cur_room
    }

    return render(
        request,
        'room.html',
        context=context
    )


def booking(request):
    bookings = Booking.objects.all()

    context = {
        'bookings': bookings
    }

    return render(
        request,
        'booking.html',
        context=context
    )
