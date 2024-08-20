# from django.shortcuts import render, redirect
# from admin__panel.models import Bus
# from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
# from .forms import AdminUserCreationForm, AdminAuthenticationForm, BusForm

# def register(request):
#     if request.method == 'POST':
#         form = AdminUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('admin__panel:admin_login')
#     else:
#         form = AdminUserCreationForm()
#     return render(request, 'admin__panel/register.html', {'form': form})

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


# # def login_view(request):
# #     if request.method == 'POST':
# #         form = AdminAuthenticationForm(request.POST)
# #         if form.is_valid():
# #             username = form.cleaned_data.get('username')
# #             password = form.cleaned_data.get('password')
# #             user = authenticate(username=username, password=password)
# #             if user is not None:
# #                 auth_login(request, user)
# #                 return redirect('admin__panel:admin_index')  # Перенаправление после входа в админку
# #     else:
# #         form = AdminAuthenticationForm()
# #     return render(request, 'admin__panel/login.html', {'form': form})

# def logout_view(request):
#     auth_logout(request)
#     return redirect('admin_login')

# def admin_index(request):
#     if request.method == 'POST':
#         form = BusForm(request.POST)
#         if form.is_valid():
#             bus = form.save(commit=False)
#             bus.admin = request.user
#             bus.save()
#             return redirect('admin__panel:admin_index')
#     else:
#         form = BusForm()
#     buses = Bus.objects.filter(admin=request.user)
#     return render(request, 'admin__panel/admin.html', {'form': form, 'buses': buses})
from django.shortcuts import render, redirect
from admin__panel.models import Bus
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import AdminUserCreationForm, AdminAuthenticationForm, BusForm

def register(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin__panel:admin_login')
    else:
        form = AdminUserCreationForm()
    return render(request, 'admin__panel/register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = AdminAuthenticationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 return redirect('admin__panel:admin_index')  # Перенаправление после входа в админку
#             else:
#                 form.add_error(None, "Invalid username or password")
#     else:
#         form = AdminAuthenticationForm()
#     return render(request, 'admin__panel/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('admin__panel:admin_login')

@login_required(login_url='admin__panel:admin_login')
def admin_index(request):
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            bus = form.save(commit=False)
            bus.admin = request.user  # Здесь должна быть проверка аутентификации
            bus.save()
            return redirect('admin__panel:admin_index')
    else:
        form = BusForm()
    buses = Bus.objects.filter(admin=request.user)
    return render(request, 'admin__panel/admin.html', {'form': form, 'buses': buses})
