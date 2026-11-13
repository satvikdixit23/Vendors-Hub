from django.db import models
from django.conf import settings
from django.utils import timezone
import json

class VendorCategory(models.TextChoices):
    SABZI = 'SABZI', '🥦 Sabziwala (Vegetables)'
    FRUITS = 'FRUITS', '🍎 Falwala (Fruits)'
    POTTERY = 'POTTERY', '🪴 Mitti ke Bartan (Clay Pottery)'
    FLOWERS = 'FLOWERS', '🌸 Phoolwala (Flowers / Pooja)'
    NEWSPAPER = 'NEWSPAPER', '📰 Akhbaar Wala (Newspaper)'
    DAIRY = 'DAIRY', '🥛 Doodh & Paneer (Dairy)'
    OTHER = 'OTHER', '🛒 General Local Vendor'

class VehicleType(models.TextChoices):
    THELA = 'THELA', 'Handcart / Thela'
    CYCLE = 'CYCLE', 'Cycle / Rickshaw'
    E_RICKSHAW = 'E_RICKSHAW', 'E-Rickshaw'
    TEMPO = 'TEMPO', 'Small Tempo / Chhota Hathi'
    ON_FOOT = 'ON_FOOT', 'On Foot'

class VendorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=150, help_text="e.g., Ramesh Sabzi Bhandar")
    category = models.CharField(max_length=20, choices=VendorCategory.choices, default=VendorCategory.SABZI)
    phone = models.CharField(max_length=15)
    upi_id = models.CharField(max_length=100, blank=True, null=True, help_text="Direct UPI ID for 0% commission customer payments")
    vehicle_type = models.CharField(max_length=20, choices=VehicleType.choices, default=VehicleType.THELA)
    
    # Area & Route Info
    city = models.CharField(max_length=100, default='New Delhi')
    area_name = models.CharField(max_length=150, help_text="e.g., Janakpuri Block B, Gali 1-7")
    pincode = models.CharField(max_length=10, default='110058')
    route_description = models.TextField(help_text="Describe your daily round, e.g. Mandir Marg -> Gali 4 -> Chungi Chowk -> Park Road")
    route_coordinates = models.TextField(blank=True, default='[]', help_text="JSON list of [lat, lng] coordinates for the route path")
    
    # Timing
    morning_slot = models.CharField(max_length=50, default="7:00 AM - 10:30 AM")
    evening_slot = models.CharField(max_length=50, default="4:30 PM - 7:30 PM", blank=True)
    is_active_today = models.BooleanField(default=True)
    status_text = models.CharField(max_length=100, default="Taking morning round in Gali 3-5", blank=True)
    
    # Promotion / Paid Listing
    is_promoted = models.BooleanField(default=False, help_text="Paid featured listing shown at the top")
    promotion_plan = models.CharField(max_length=50, default="None")
    promotion_expires_at = models.DateTimeField(null=True, blank=True)
    
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.8)
    total_orders = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_currently_promoted(self):
        if not self.is_promoted:
            return False
        if self.promotion_expires_at and self.promotion_expires_at < timezone.now():
            return False
        return True

    def get_route_points(self):
        try:
            return json.loads(self.route_coordinates)
        except Exception:
            return []

    def __str__(self):
        return f"{self.business_name} ({self.get_category_display()}) - {self.area_name}"

class Product(models.Model):
    UNIT_CHOICES = (
        ('kg', 'per kg'),
        ('500g', 'per 500g'),
        ('250g', 'per 250g'),
        ('piece', 'per piece'),
        ('dozen', 'per dozen'),
        ('bundle', 'per bundle / gaddi'),
        ('packet', 'per packet'),
        ('month', 'monthly subscription'),
    )

    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=120, help_text="Product name in English")
    hindi_name = models.CharField(max_length=120, blank=True, help_text="Product name in Hindi")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='kg')
    is_available = models.BooleanField(default=True)
    emoji_icon = models.CharField(max_length=10, default='🛒')
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}/{self.unit} ({self.vendor.business_name})"

class PromotionPlan(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=150)
    price = models.IntegerField(help_text="Price in INR")
    duration_days = models.IntegerField(default=30)
    badge_label = models.CharField(max_length=50, default="⭐ Featured")
    benefits = models.TextField(help_text="Comma separated list of benefits")
    is_popular = models.BooleanField(default=False)

    def get_benefits_list(self):
        return [b.strip() for b in self.benefits.split(',') if b.strip()]

    def __str__(self):
        return f"{self.name} - ₹{self.price} for {self.duration_days} days"
