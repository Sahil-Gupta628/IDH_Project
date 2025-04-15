# prescriptions/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('scan/', views.scan_view, name='scan'),
    path('view_scan/<int:scan_id>/', views.view_scan, name='view_scan'),
    path('get_scan/<int:scan_id>/', views.get_scan_json, name='get_scan_json'),
]