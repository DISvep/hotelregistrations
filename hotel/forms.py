from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Booking, Room, Review


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "username"})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'password'})


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.TextInput(attrs={
                'class': 'flatpickr form-control'
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'flatpickr form-control'
            })
        }


class RoomFilterForm(forms.Form):
    CLASSES_CHOICES = [
        ('', "Оберіть клас житла"),
        ('_economy', 'Економ'),
        ('_comfort', 'Комфорт'),
        ('_business', "Бізнес"),
        ('_premium', 'Преміум')
    ]

    minimum_price = forms.IntegerField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': "form-control me-2", "placeholder": 'Мінімальна ціна', 'aria-label': "Search"})
    )
    maximum_price = forms.IntegerField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={'class': "form-control me-2", "placeholder": 'Максимальна ціна', 'aria-label': "Search"}),
    )
    classes = forms.ChoiceField(
        choices=CLASSES_CHOICES,
        required=False,
        label='',
        widget=forms.Select(attrs={'class': "form-control me-2", 'aria-label': "Search"})
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {'rating': ''}
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'id': 'rating_input',
                'min': 1,
                'max': 10,
                'step': 1,
                'placeholder': 'Enter rating (1-10)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'cols': 50,
                'placeholder': 'Type review...'
            })
        }
