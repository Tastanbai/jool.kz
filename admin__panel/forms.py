from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from admin__panel.models import Bus

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AdminAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class BusForm(forms.ModelForm):
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    departure_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Bus
        fields = ['number', 'from_location', 'to_location', 'departure_date', 'departure_time', 'seats', 'price',  'bus_type']

        from django import forms
from .models import Seat

class SeatSelectionForm(forms.Form):
    seat = forms.ModelChoiceField(queryset=Seat.objects.none())
    full_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        bus = kwargs.pop('bus', None)
        super().__init__(*args, **kwargs)
        if bus:
            self.fields['seat'].queryset = bus.get_free_seats()

