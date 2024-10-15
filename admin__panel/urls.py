from django.urls import path
from . import views

app_name = 'admin__panel'

urlpatterns = [
    path('login/', views.login_view, name='admin_login'),  
    path('logout/', views.logout_view, name='admin_logout'),
    path('register/', views.register, name='admin_register'),
    path('', views.admin_index, name='admin_index'),
    path('get_passengers/<int:bus_id>/', views.get_passengers, name='get_passengers'),
]
