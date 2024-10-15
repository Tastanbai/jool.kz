from django.shortcuts import render, redirect
from admin__panel.models import Bus
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import AdminUserCreationForm, AdminAuthenticationForm, BusForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Bus, Seat

def login_view(request):
    if request.method == 'POST':
        form = AdminAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('admin__panel:admin_index')  # Перенаправление после входа в админку
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AdminAuthenticationForm()
    return render(request, 'admin__panel/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin__panel:admin_login')
    else:
        form = AdminUserCreationForm()
    return render(request, 'admin__panel/register.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('admin__panel:admin_login')


@login_required(login_url='admin__panel:admin_login')
def admin_index(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            bus = form.save(commit=False)
            bus.admin = request.user
            bus.save()
            return redirect('admin__panel:admin_index')
        else:
            print(f"Form errors: {form.errors}") 
    else:
        form = BusForm()
    
    buses = Bus.objects.filter(admin=request.user).select_related('admin')
    
    return render(request, 'admin__panel/admin.html', {
        'form': form,
        'buses': buses,
    })

@login_required
def get_passengers(request, bus_id):
    try:
        bus = Bus.objects.select_related('admin').get(id=bus_id, admin=request.user)
        passengers = Seat.objects.filter(bus=bus, is_reserved=True).values(
            'seat_number', 'reserved_by', 'reserved_phone', 'reserved_email'
        )
        return JsonResponse(list(passengers), safe=False)
    except Bus.DoesNotExist:
        return JsonResponse({'error': 'Bus not found'}, status=404)