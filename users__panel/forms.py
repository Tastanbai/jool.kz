from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Форма регистрации с русскими метками
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

# Форма входа с русскими метками
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'Имя пользователя',
            'password': 'Пароль',
        }

from admin__panel.models import Seat

# Форма выбора мест с русскими метками
class SeatSelectionForm(forms.Form):
    seat = forms.ModelChoiceField(queryset=Seat.objects.none(), label="Выбор места")
    full_name = forms.CharField(max_length=255, label="Полное имя")
    phone_number = forms.CharField(max_length=15, label="Номер телефона")
    email = forms.EmailField(label="Электронная почта")

    def __init__(self, *args, **kwargs):
        bus = kwargs.pop('bus', None)
        super().__init__(*args, **kwargs)
        if bus:
            # Настройка для выбора только свободных мест
            self.fields['seat'].queryset = bus.get_free_seats()
