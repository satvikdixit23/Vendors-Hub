from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='vendor_dashboard'),
    path('dashboard/route/', views.route_manager_view, name='vendor_route_manager'),
    path('dashboard/products/', views.product_manager_view, name='vendor_product_manager'),
    path('dashboard/products/toggle/<int:product_id>/', views.toggle_product_availability, name='vendor_toggle_product'),
    path('dashboard/products/delete/<int:product_id>/', views.delete_product, name='vendor_delete_product'),
    path('dashboard/products/quick-stock/', views.quick_stock_products, name='vendor_quick_stock'),
    path('dashboard/orders/', views.orders_view, name='vendor_orders'),
    path('dashboard/orders/<int:order_id>/update/', views.update_order_status, name='vendor_update_order_status'),
    path('dashboard/promotions/', views.promotions_view, name='vendor_promotions'),
    path('dashboard/promotions/activate/<int:plan_id>/', views.activate_promotion, name='vendor_activate_plan'),
    path('storefront/<int:vendor_id>/', views.storefront_view, name='vendor_storefront'),
    path('api/map-data/', views.api_vendors_map, name='api_vendors_map'),
]
