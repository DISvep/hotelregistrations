from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Floor, Room, Booking
from .forms import UserRegistrationForm, BookingForm


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


@login_required
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


@login_required
def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking_ = form.save(commit=False)
            booking_.user = request.user
            booking_.save()

            return redirect('booking')
        else:
            return render(
                request,
                'booking_form.html',
                {'form': form}
            )
    else:
        form = BookingForm(request.POST)

        return render(
            request,
            'booking_form.html',
            {'form': form}
        )


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('/')
        else:
            return render(
                request,
                'register.html',
                {'form': form}
            )
    else:
        form = UserRegistrationForm()

        return render(
            request,
            "register.html",
            {"form": form}
        )
