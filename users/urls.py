from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('demo-login/<str:role>/', views.demo_login_view, name='demo_login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
