from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Floor, Room, Booking, Review
from .forms import UserRegistrationForm, BookingForm, LoginForm, ReviewForm
from django.contrib.auth.views import LoginView
from datetime import timedelta
from django.db.models import Count
from django.utils import timezone


# Create your views here.
def index(request):
    floors = Floor.objects.all()
    rooms = Room.objects.all()
    with_discounts = Room.objects.all().filter(discount__isnull=False)
    popular = Room.objects.annotate(review_count=Count('reviews')).filter(review_count__gte=10, rating__gte=5.0)
    # popular = Room.objects.all().filter(rating__gt=5.0, reviews_count__gte=10).distinct()
    grouped_discounts = [
        with_discounts[i:i + 4] for i in range(0, len(with_discounts), 4)
    ]
    grouped_popular = [
        popular[i:i + 4] for i in range(0, len(popular), 4)
    ]

    context = {
        'floors': floors,
        'rooms': rooms,
        'grouped_discounts': grouped_discounts,
        'grouped_popular': grouped_popular
    }

    return render(
        request,
        'index.html',
        context=context
    )


def economy(request):
    rooms = Room.objects.all().filter(classes='_economy')

    context = {
        'rooms': rooms
    }

    return render(
        request,
        'economy.html',
        context=context
    )


def comfort(request):
    rooms = Room.objects.all().filter(classes='_comfort')

    context = {
        'rooms': rooms
    }

    return render(
        request,
        'comfort.html',
        context=context
    )


def business(request):
    rooms = Room.objects.all().filter(classes='_business')

    context = {
        'rooms': rooms
    }

    return render(
        request,
        'business.html',
        context=context
    )


def premium(request):
    rooms = Room.objects.all().filter(classes='_premium')

    context = {
        'rooms': rooms
    }

    return render(
        request,
        'premium.html',
        context=context
    )


def room(request, room_id):
    cur_room = Room.objects.filter(id=room_id).first()
    reviews = cur_room.reviews.all()
    bookings = cur_room.booking.all()

    for booking_ in bookings:
        if booking_.status != '_cancelled':
            if booking_.end_time < timezone.now().date():
                booking_.status = "_done"
                booking_.save()
            elif timezone.now().date() < booking_.start_time:
                booking_.status = '_waiting'
                booking_.save()
            else:
                booking_.status = '_active'
                booking_.save()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.room = cur_room
            review.save()

            return redirect('room', room_id=cur_room.id)
        else:
            return redirect('room', room_id=cur_room.id)
    else:
        form = ReviewForm()

    context = {
        'room': cur_room,
        'review_form': form,
        'reviews': reviews,
        'bookings': bookings
    }

    return render(
        request,
        'room.html',
        context=context
    )


def search_results(request):
    minimum_price = request.GET.get('minimum_price', None)
    maximum_price = request.GET.get('maximum_price', None)
    classes = request.GET.get('classes', None)

    rooms = Room.objects.all()
    if minimum_price:
        rooms = rooms.filter(price__gte=minimum_price)
    if maximum_price:
        rooms = rooms.filter(price__lte=maximum_price)
    if classes:
        rooms = rooms.filter(classes=classes)

    context = {'rooms': rooms}
    return render(request, 'search_results.html', context=context)


@login_required
def delete_booking(request, booking_id):
    booking_ = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking_.delete()

        return redirect('/')

    return render(request, 'confirm_delete.html', {'booking': booking_, 'not_welcome': True})


@login_required
def create_booking(request, room_id):
    room_ = Room.objects.filter(id=room_id).first()
    if not room:
        return redirect('error_page')

    blocked_bookings = Booking.objects.filter(room=room_)
    blocked_dates = []

    for booking_ in blocked_bookings:
        current_date = booking_.start_time
        while current_date <= booking_.end_time:
            blocked_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking_ = form.save(commit=False)
            booking_.user = request.user
            booking_.room = Room.objects.all().filter(id=room_id).first()
            booking_.status = "_active"
            same_room = Booking.objects.all().filter(room=booking_.room)

            for room_ in same_room:
                if (
                        room_.start_time <= booking_.start_time <= room_.end_time or
                        room_.start_time <= booking_.end_time <= room_.end_time or
                        (booking_.start_time <= room_.start_time and booking_.end_time >= room_.end_time)
                ):
                    return render(
                        request,
                        'booking_form.html',
                        {
                            'form': form,
                            "message": "Вже є така заброньована кімната у рамках вашого часу",
                            'blocked_dates': blocked_dates,
                            "not_welcome": True
                        }
                    )

            booking_.save()

            return redirect('room', room_id=booking_.room.id)
        else:
            return render(
                request,
                'booking_form.html',
                {'form': form, "message": "", 'blocked_dates': blocked_dates, "not_welcome": True}
            )
    else:
        form = BookingForm(request.POST)

        return render(
            request,
            'booking_form.html',
            {'form': form, "message": "", "not_welcome": True, 'blocked_dates': blocked_dates, }
        )


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_welcome'] = True
        return context


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
                {'form': form, "not_welcome": True}
            )
    else:
        form = UserRegistrationForm()

        return render(
            request,
            "register.html",
            {"form": form, "not_welcome": True}
        )
