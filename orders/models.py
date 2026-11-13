from django.db import models
from django.conf import settings
from vendors.models import VendorProfile, Product
import uuid

class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', '⏳ Order Placed (Waiting for Vendor)'
    ACCEPTED = 'ACCEPTED', '✅ Accepted by Vendor'
    ON_THE_WAY = 'ON_THE_WAY', '🚴 In Vendor Route / Out for Delivery'
    DELIVERED = 'DELIVERED', '🎉 Delivered'
    CANCELLED = 'CANCELLED', '❌ Cancelled'

class PaymentMethod(models.TextChoices):
    COD = 'COD', '💵 Cash on Delivery (0% Commission)'
    UPI_DIRECT = 'UPI_DIRECT', '📱 Direct UPI to Vendor Cart (0% Commission)'

class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_orders')
    
    # Customer Details for Delivery
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=15)
    delivery_address = models.CharField(max_length=255, help_text="House/Flat No., Gali No., Landmark")
    delivery_area = models.CharField(max_length=150, help_text="Colony / Mohalla / Area")
    
    # Scheduling Details
    delivery_date = models.DateField()
    delivery_slot = models.CharField(max_length=100, help_text="e.g., Morning Round (7:30 AM - 9:00 AM)")
    
    # Payment & Financials
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.COD)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    special_instructions = models.TextField(blank=True, help_text="e.g. Ring bell twice, bring fresh items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = "VH-" + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_id} - {self.customer_name} -> {self.vendor.business_name} (₹{self.total_amount})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=150)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20, default='kg')
    quantity = models.DecimalField(max_digits=6, decimal_places=2, default=1.0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity} {self.unit} (₹{self.subtotal})"
