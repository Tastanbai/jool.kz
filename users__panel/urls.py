from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search-buses/', views.search_buses, name='search_buses'),
    path('bus/<int:bus_id>/', views.bus_detail, name='bus_detail'),
    path('login/', views.login_view, name='login'),  # Обновляем маршрут
    path('logout/', views.logout_view, name='logout'),  # Обновляем маршрут
    path('register/', views.register, name='register'),
    path('kaspi-payment/', views.kaspi_payment, name='kaspi_payment'),
]
