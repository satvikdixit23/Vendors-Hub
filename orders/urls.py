from django.urls import path
from . import views

urlpatterns = [
    path('place/<int:vendor_id>/', views.place_order_view, name='place_order'),
    path('track/<str:order_id>/', views.order_detail_view, name='order_detail'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
]
