from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:plan_id>/', views.checkout_view, name='checkout'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
]
