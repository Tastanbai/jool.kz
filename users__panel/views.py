from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from admin__panel.models import Bus, Seat
from .forms import CustomUserCreationForm, CustomAuthenticationForm, SeatSelectionForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users__panel/register.html', {'form': form})

def login_view(request):  # Переименуем представление
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)  # Передаем request
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  # Передаем request
            if user is not None:
                login(request, user)  # Функция login вызывается с параметрами request и user
                return redirect('index')  # Перенаправляем пользователя на главную страницу
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users__panel/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'users__panel/index.html')

def search_buses(request):
    from_location = request.GET.get('from')
    to_location = request.GET.get('to')
    departure_date = request.GET.get('departure_date')
    bus_type = request.GET.get('bus_type')

    # Изначально фильтруем все автобусы
    buses = Bus.objects.all()

    # Фильтрация по каждому критерию, если он был введен
    if from_location:
        buses = buses.filter(from_location__iexact=from_location)
    if to_location:
        buses = buses.filter(to_location__iexact=to_location)
    if departure_date:
        buses = buses.filter(departure_date=departure_date)

    # Если автобусы не найдены, показываем сообщение
    if not buses.exists():
        message = "Нет доступных автобусов по вашему запросу."
        buses = None
    else:
        message = None

    return render(request, 'users__panel/index.html', {'buses': buses, 'message': message})

# def bus_detail(request, bus_id):
#     bus = get_object_or_404(Bus, pk=bus_id)
#     seats = Seat.objects.filter(bus=bus)

#     if request.method == 'POST':
#         form = SeatSelectionForm(request.POST, bus=bus)
#         if form.is_valid():
#             seat = form.cleaned_data['seat']
#             if not seat.is_reserved:
#                 seat.is_reserved = True
#                 seat.reserved_by = form.cleaned_data['full_name']
#                 seat.reserved_phone = form.cleaned_data['phone_number']
#                 seat.reserved_email = form.cleaned_data['email']
#                 seat.save()
#                 return redirect('bus_detail', bus_id=bus.id)
#             else:
#                 form.add_error('seat', 'Это место уже занято. Пожалуйста, выберите другое.')
#     else:
#         form = SeatSelectionForm(bus=bus)

#     return render(request, 'users__panel/bus_detail.html', {'bus': bus, 'seats': seats, 'form': form})


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from admin__panel.models import Bus, Seat
from .forms import SeatSelectionForm

@login_required(login_url='login')  # Требуется авторизация
def bus_detail(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    seats = Seat.objects.filter(bus=bus)

    if request.method == 'POST':
        form = SeatSelectionForm(request.POST, bus=bus)
        if form.is_valid():
            seat = form.cleaned_data['seat']
            if not seat.is_reserved:
                seat.is_reserved = True
                seat.reserved_by = form.cleaned_data['full_name']
                seat.reserved_phone = form.cleaned_data['phone_number']
                seat.reserved_email = form.cleaned_data['email']
                seat.save()
                return redirect('bus_detail', bus_id=bus.id)
            else:
                form.add_error('seat', 'Это место уже занято. Пожалуйста, выберите другое.')
    else:
        form = SeatSelectionForm(bus=bus)

    return render(request, 'users__panel/bus_detail.html', {'bus': bus, 'seats': seats, 'form': form})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def kaspi_payment(request):
    txn_id = request.GET.get('txn_id')
    command = request.GET.get('command')
    account = request.GET.get('account')
    sum = request.GET.get('sum')
    
    if command == 'check':
        # Проверяем существование аккаунта и его состояние
        response_data = {
            "txn_id": txn_id,
            "result": 0,
            "comment": "Аккаунт существует и готов к оплате"
        }
    elif command == 'pay':
        # Обработка платежа и сохранение данных
        response_data = {
            "txn_id": txn_id,
            "prv_txn": 123456,  # Уникальный номер оплаты в вашей системе
            "result": 0,
            "sum": sum,
            "comment": "Оплата успешно проведена"
        }
    else:
        response_data = {
            "txn_id": txn_id,
            "result": 5,
            "comment": "Неизвестная команда"
        }
    
    return JsonResponse(response_data)


