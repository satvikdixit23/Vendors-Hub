from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from decimal import Decimal
from .models import Order, OrderItem, OrderStatus, PaymentMethod
from vendors.models import VendorProfile, Product

def place_order_view(request, vendor_id):
    vendor = get_object_or_404(VendorProfile, id=vendor_id)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        delivery_address = request.POST.get('delivery_address')
        delivery_area = request.POST.get('delivery_area', vendor.area_name)
        delivery_date = request.POST.get('delivery_date')
        delivery_slot = request.POST.get('delivery_slot', vendor.morning_slot)
        payment_method = request.POST.get('payment_method', PaymentMethod.COD)
        special_instructions = request.POST.get('special_instructions', '')
        
        cart_data_raw = request.POST.get('cart_items', '[]')
        try:
            cart_items = json.loads(cart_data_raw)
        except Exception:
            cart_items = []

        if not cart_items:
            messages.error(request, "Your cart is empty! Please add products before placing an order.")
            return redirect('vendor_storefront', vendor_id=vendor.id)

        # Calculate total and validate items
        total_amount = Decimal('0.00')
        valid_order_items = []

        for item in cart_items:
            product_id = item.get('product_id')
            qty = Decimal(str(item.get('quantity', 1)))
            product = Product.objects.filter(id=product_id, vendor=vendor).first()
            if product:
                subtotal = product.price * qty
                total_amount += subtotal
                valid_order_items.append({
                    'product': product,
                    'name': product.name,
                    'price': product.price,
                    'unit': product.unit,
                    'quantity': qty,
                    'subtotal': subtotal
                })

        if not valid_order_items:
            messages.error(request, "No valid items found in cart.")
            return redirect('vendor_storefront', vendor_id=vendor.id)

        # Create Order
        customer_user = request.user if request.user.is_authenticated else None
        
        order = Order.objects.create(
            vendor=vendor,
            customer=customer_user,
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_address=delivery_address,
            delivery_area=delivery_area,
            delivery_date=delivery_date or timezone.now().date(),
            delivery_slot=delivery_slot,
            payment_method=payment_method,
            total_amount=total_amount,
            special_instructions=special_instructions,
            status=OrderStatus.PENDING
        )

        for vi in valid_order_items:
            OrderItem.objects.create(
                order=order,
                product=vi['product'],
                product_name=vi['name'],
                unit_price=vi['price'],
                unit=vi['unit'],
                quantity=vi['quantity'],
                subtotal=vi['subtotal']
            )

        messages.success(request, f"🎉 Order placed successfully with {vendor.business_name}! Thela will arrive during your scheduled time slot.")
        return redirect('order_detail', order_id=order.order_id)

    return redirect('vendor_storefront', vendor_id=vendor.id)

def order_detail_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    # Generate WhatsApp message link for direct vendor communication
    wa_text = f"Namaste {order.vendor.business_name}, I have placed order #{order.order_id} on Vendor's Hub for {order.delivery_slot}. Total: Rs.{order.total_amount}. Address: {order.delivery_address}"
    wa_url = f"https://wa.me/91{order.vendor.phone}?text={wa_text.replace(' ', '%20')}"

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': order.items.all(),
        'wa_url': wa_url
    })

@login_required
def my_orders_view(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {
        'orders': orders
    })
