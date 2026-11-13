from django.shortcuts import render
from vendors.models import VendorProfile, VendorCategory, PromotionPlan
import json

def home(request):
    area_query = request.GET.get('area', '').strip()
    category_filter = request.GET.get('category', '').strip()

    # Base active vendors
    vendors_qs = VendorProfile.objects.filter(is_active_today=True)

    if area_query:
        vendors_qs = vendors_qs.filter(
            models_q(area_query)
        )

    if category_filter:
        vendors_qs = vendors_qs.filter(category=category_filter)

    # Sort so Promoted / Paid listings appear first, then highest rating
    all_vendors = list(vendors_qs.order_by('-is_promoted', '-rating', '-total_orders'))

    # Separate featured / promoted vendors for the top carousel/banner
    promoted_vendors = [v for v in all_vendors if v.is_currently_promoted()]
    
    # Map points for Leaflet
    map_vendors_data = []
    for v in all_vendors:
        points = v.get_route_points()
        map_vendors_data.append({
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

    categories = VendorCategory.choices
    plans = PromotionPlan.objects.all().order_by('price')

    return render(request, 'core/home.html', {
        'vendors': all_vendors,
        'promoted_vendors': promoted_vendors,
        'categories': categories,
        'selected_category': category_filter,
        'area_query': area_query,
        'map_vendors_json': json.dumps(map_vendors_data),
        'plans': plans
    })

def models_q(area_query):
    from django.db.models import Q
    return (
        Q(area_name__icontains=area_query) |
        Q(city__icontains=area_query) |
        Q(pincode__icontains=area_query) |
        Q(route_description__icontains=area_query)
    )
