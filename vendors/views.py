from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json
from .models import VendorProfile, Product, PromotionPlan, VendorCategory, VehicleType
from orders.models import Order, OrderStatus

def vendor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'vendor_profile'):
            messages.error(request, "This area is only for registered vendors.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@vendor_required
def dashboard_view(request):
    vendor = request.user.vendor_profile
    orders = vendor.orders.all().order_by('-created_at')
    
    today = timezone.now().date()
    today_orders = orders.filter(delivery_date=today)
    pending_orders = orders.filter(status=OrderStatus.PENDING)
    
    total_revenue = sum(o.total_amount for o in orders.filter(status=OrderStatus.DELIVERED))

    # Toggle active status or status text
    if request.method == 'POST' and 'update_status' in request.POST:
        vendor.status_text = request.POST.get('status_text', vendor.status_text)
        vendor.is_active_today = ('is_active_today' in request.POST)
        vendor.save()
        messages.success(request, "Thela status updated!")
        return redirect('vendor_dashboard')

    return render(request, 'vendors/dashboard.html', {
        'vendor': vendor,
        'recent_orders': orders[:5],
        'today_orders_count': today_orders.count(),
        'pending_orders_count': pending_orders.count(),
        'total_revenue': total_revenue,
        'total_products': vendor.products.count()
    })

@login_required
@vendor_required
def route_manager_view(request):
    vendor = request.user.vendor_profile

    if request.method == 'POST':
        vendor.area_name = request.POST.get('area_name', vendor.area_name)
        vendor.city = request.POST.get('city', vendor.city)
        vendor.pincode = request.POST.get('pincode', vendor.pincode)
        vendor.morning_slot = request.POST.get('morning_slot', vendor.morning_slot)
        vendor.evening_slot = request.POST.get('evening_slot', vendor.evening_slot)
        vendor.route_description = request.POST.get('route_description', vendor.route_description)
        vendor.vehicle_type = request.POST.get('vehicle_type', vendor.vehicle_type)
        
        coords_raw = request.POST.get('route_coordinates', '')
        if coords_raw:
            try:
                # Validate json format
                json.loads(coords_raw)
                vendor.route_coordinates = coords_raw
            except Exception:
                pass

        vendor.save()
        messages.success(request, "Route and Mohalla schedule updated successfully!")
        return redirect('vendor_route_manager')

    return render(request, 'vendors/route_manager.html', {
        'vendor': vendor,
        'vehicles': VehicleType.choices,
        'route_points_json': vendor.route_coordinates or '[]'
    })

@login_required
@vendor_required
def product_manager_view(request):
    vendor = request.user.vendor_profile
    products = vendor.products.all().order_by('-created_at')

    # Add product form
    if request.method == 'POST' and 'add_product' in request.POST:
        name = request.POST.get('name')
        hindi_name = request.POST.get('hindi_name', '')
        price = request.POST.get('price')
        unit = request.POST.get('unit', 'kg')
        emoji = request.POST.get('emoji_icon', '🛒')
        desc = request.POST.get('description', '')

        Product.objects.create(
            vendor=vendor,
            name=name,
            hindi_name=hindi_name,
            price=price,
            unit=unit,
            emoji_icon=emoji,
            description=desc,
            is_available=True
        )
        messages.success(request, f"Added '{name}' to your cart inventory!")
        return redirect('vendor_product_manager')

    return render(request, 'vendors/product_manager.html', {
        'vendor': vendor,
        'products': products,
        'unit_choices': Product.UNIT_CHOICES
    })

@login_required
@vendor_required
def toggle_product_availability(request, product_id):
    vendor = request.user.vendor_profile
    product = get_object_or_404(Product, id=product_id, vendor=vendor)
    product.is_available = not product.is_available
    product.save()
    status_str = "Available" if product.is_available else "Out of Stock"
    messages.info(request, f"{product.name} is now marked as {status_str}.")
    return redirect('vendor_product_manager')

@login_required
@vendor_required
def delete_product(request, product_id):
    vendor = request.user.vendor_profile
    product = get_object_or_404(Product, id=product_id, vendor=vendor)
    name = product.name
    product.delete()
    messages.warning(request, f"Removed '{name}' from inventory.")
    return redirect('vendor_product_manager')

@login_required
@vendor_required
def quick_stock_products(request):
    """Adds standard template items matching the vendor's category"""
    vendor = request.user.vendor_profile
    cat = vendor.category
    
    defaults_map = {
        'SABZI': [
            ("Lal Tamatar (Tomato)", "टमाटर", 35, "kg", "🍅"),
            ("Aloo (Potato)", "आलू", 25, "kg", "🥔"),
            ("Pyaaz (Onion)", "प्याज", 40, "kg", "🧅"),
            ("Hari Mirch & Dhaniya", "धनिया मिर्च", 15, "bundle", "🌿"),
            ("Adrak (Ginger)", "अदरक", 20, "250g", "🫚"),
            ("Shimla Mirch", "शिमला मिर्च", 50, "kg", "🫑"),
        ],
        'FRUITS': [
            ("Kela (Bananas)", "केला", 50, "dozen", "🍌"),
            ("Kashmiri Seb (Apples)", "सेब", 120, "kg", "🍎"),
            ("Mithas Santra (Oranges)", "संतरा", 60, "kg", "🍊"),
            ("Pomegranate (Anar)", "अनार", 140, "kg", "🥭"),
        ],
        'POTTERY': [
            ("Clay Water Matka", "मिट्टी का मटका", 180, "piece", "🏺"),
            ("Kulhad Set (6 pcs)", "कुल्हड़", 60, "bundle", "☕"),
            ("Mitti Handi", "मिट्टी हांडी", 150, "piece", "🍲"),
        ],
        'FLOWERS': [
            ("Genda Mala (Garland)", "गेंदा माला", 30, "piece", "🌼"),
            ("Gulab Phool (Roses)", "गुलाब फूल", 50, "bundle", "🌹"),
            ("Pooja Samagri Combo", "पूजा पत्ता", 25, "packet", "🍃"),
        ],
        'NEWSPAPER': [
            ("Dainik Jagran", "दैनिक जागरण", 150, "month", "📰"),
            ("The Times of India", "टाइम्स ऑफ़ इंडिया", 200, "month", "🗞️"),
            ("Hindustan Times", "हिन्दुस्तान टाइम्स", 180, "month", "📰"),
        ]
    }

    items = defaults_map.get(cat, defaults_map['SABZI'])
    added_count = 0
    for name, hname, price, unit, emoji in items:
        if not Product.objects.filter(vendor=vendor, name=name).exists():
            Product.objects.create(
                vendor=vendor,
                name=name,
                hindi_name=hname,
                price=price,
                unit=unit,
                emoji_icon=emoji,
                is_available=True
            )
            added_count += 1

    messages.success(request, f"Quick Stock added {added_count} standard products to your thela!")
    return redirect('vendor_product_manager')

@login_required
@vendor_required
def orders_view(request):
    vendor = request.user.vendor_profile
    status_filter = request.GET.get('status')
    
    orders = vendor.orders.all().order_by('-delivery_date', '-created_at')
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'vendors/orders.html', {
        'vendor': vendor,
        'orders': orders,
        'status_choices': OrderStatus.choices,
        'current_filter': status_filter
    })

@login_required
@vendor_required
def update_order_status(request, order_id):
    vendor = request.user.vendor_profile
    order = get_object_or_404(Order, id=order_id, vendor=vendor)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in OrderStatus.values:
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.order_id} status updated to {order.get_status_display()}!")
    
    return redirect('vendor_orders')

@login_required
@vendor_required
def promotions_view(request):
    vendor = request.user.vendor_profile
    plans = PromotionPlan.objects.all().order_by('price')

    return render(request, 'vendors/promotions.html', {
        'vendor': vendor,
        'plans': plans
    })

@login_required
@vendor_required
def activate_promotion(request, plan_id):
    """Simulates payment & activation of paid promotional listing"""
    vendor = request.user.vendor_profile
    plan = get_object_or_404(PromotionPlan, id=plan_id)

    vendor.is_promoted = True
    vendor.promotion_plan = plan.name
    vendor.promotion_expires_at = timezone.now() + timedelta(days=plan.duration_days)
    vendor.save()

    messages.success(request, f"🎉 Congratulations! '{plan.name}' plan is now active for {plan.duration_days} days. Your cart will now appear at the top of customer search!")
    return redirect('vendor_promotions')

def storefront_view(request, vendor_id):
    """Public customer-facing storefront for a specific vendor"""
    vendor = get_object_or_404(VendorProfile, id=vendor_id)
    products = vendor.products.filter(is_available=True)
    
    return render(request, 'vendors/storefront.html', {
        'vendor': vendor,
        'products': products,
        'route_points_json': vendor.route_coordinates or '[]'
    })

def api_vendors_map(request):
    """API endpoint returning vendors on active routes with coordinates for map display"""
    area = request.GET.get('area', '')
    category = request.GET.get('category', '')

    vendors = VendorProfile.objects.filter(is_active_today=True)
    if area:
        vendors = vendors.filter(area_name__icontains=area) | vendors.filter(city__icontains=area) | vendors.filter(pincode__icontains=area)
    if category:
        vendors = vendors.filter(category=category)

    data = []
    for v in vendors:
        points = v.get_route_points()
        data.append({
            'id': v.id,
            'name': v.business_name,
            'category': v.get_category_display(),
            'phone': v.phone,
            'vehicle': v.get_vehicle_type_display(),
            'area': v.area_name,
            'morning_slot': v.morning_slot,
            'evening_slot': v.evening_slot,
            'status_text': v.status_text,
            'is_promoted': v.is_currently_promoted(),
            'rating': float(v.rating),
            'route_points': points,
            'store_url': f"/vendor/storefront/{v.id}/"
        })
    return JsonResponse({'vendors': data})
