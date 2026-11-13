from django.core.management.base import BaseCommand
from users.models import CustomUser
from vendors.models import VendorProfile, Product, PromotionPlan, VendorCategory, VehicleType
from orders.models import Order, OrderItem, OrderStatus, PaymentMethod
from django.utils import timezone
from datetime import timedelta
import json

class Command(BaseCommand):
    help = "Seed Vendor's Hub with realistic Indian vendors, routes, products, orders, and promotion plans"

    def handle(self, *args, **options):
        self.stdout.write("Seeding initial data...")

        # 1. Create Promotion Plans
        plan1, _ = PromotionPlan.objects.get_or_create(
            name="Gali Starter",
            defaults={
                "tagline": "Ideal for new thelawalas starting in one colony",
                "price": 49,
                "duration_days": 7,
                "badge_label": "⭐ Verified Gali Vendor",
                "benefits": "Colony route highlight, Direct phone calls, 0% commission, 7 days featured",
                "is_popular": False
            }
        )
        plan2, _ = PromotionPlan.objects.get_or_create(
            name="Mohalla Star",
            defaults={
                "tagline": "Top visibility across 10-15 galis and major chowks",
                "price": 149,
                "duration_days": 30,
                "badge_label": "👑 Mohalla Gold Top Vendor",
                "benefits": "Top position in customer search, Golden crown badge, Live route tracker badge, Priority scheduled orders, WhatsApp direct connect",
                "is_popular": True
            }
        )
        plan3, _ = PromotionPlan.objects.get_or_create(
            name="City Booster",
            defaults={
                "tagline": "Complete area domination with multi-colony routes",
                "price": 499,
                "duration_days": 90,
                "badge_label": "🔥 Area Champion",
                "benefits": "Full city search highlight, Featured banner on homepage, Unlimited products, Dedicated support, SMS alerts to regular customers",
                "is_popular": False
            }
        )

        # 2. Create Users (Vendors, Customers, Admin)
        admin_user, _ = CustomUser.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True, "email": "admin@vendorshub.in"}
        )
        admin_user.set_password("admin123")
        admin_user.save()

        # Customer User
        cust_user, _ = CustomUser.objects.get_or_create(
            username="customer_pooja",
            defaults={
                "user_type": "CUSTOMER",
                "phone": "9876543210",
                "email": "pooja@example.com",
                "first_name": "Pooja",
                "last_name": "Sharma",
                "address": "Flat 204, Shanti Apartments, Gali No. 4, Janakpuri"
            }
        )
        cust_user.set_password("password123")
        cust_user.save()

        # Vendor 1: Ramesh Sabziwala
        v1_user, _ = CustomUser.objects.get_or_create(
            username="vendor_ramesh",
            defaults={
                "user_type": "VENDOR",
                "phone": "9811223344",
                "email": "ramesh.sabzi@example.com",
                "first_name": "Ramesh",
                "last_name": "Kumar"
            }
        )
        v1_user.set_password("password123")
        v1_user.save()

        v1_profile, _ = VendorProfile.objects.get_or_create(
            user=v1_user,
            defaults={
                "business_name": "Ramesh Desi Sabzi Bhandar",
                "category": VendorCategory.SABZI,
                "phone": "9811223344",
                "upi_id": "rameshsabzi@upi",
                "vehicle_type": VehicleType.THELA,
                "city": "New Delhi",
                "area_name": "Janakpuri Block B, Gali 1 to 9",
                "pincode": "110058",
                "route_description": "Shuruat Mandir Mod -> Gali No. 1 -> Chungi Road -> DDA Community Park -> Gali No. 8 & 9 Chowk",
                "route_coordinates": json.dumps([
                    [28.6219, 77.0878],
                    [28.6235, 77.0895],
                    [28.6250, 77.0912],
                    [28.6268, 77.0890],
                    [28.6285, 77.0872]
                ]),
                "morning_slot": "7:00 AM - 10:30 AM",
                "evening_slot": "5:00 PM - 7:30 PM",
                "is_active_today": True,
                "status_text": "🥦 Abhi Gali No. 3 mein taaza tamatar aur gobhi lekar pahunch rahe hain!",
                "is_promoted": True,
                "promotion_plan": "Mohalla Star",
                "promotion_expires_at": timezone.now() + timedelta(days=25),
                "rating": 4.9,
                "total_orders": 142
            }
        )

        # Products for Ramesh Sabziwala
        sabzi_items = [
            ("Desi Lal Tamatar (Tomato)", "लाल टमाटर", 35, "kg", "🍅", "Ekdum taaza local khet ka tamatar"),
            ("Pahadi Aloo (Potatoes)", "पहाड़ी नया आलू", 25, "kg", "🥔", "Bina mitti ka saaf pahadi aloo"),
            ("Nashik Pyaaz (Onions)", "नासिक प्याज", 40, "kg", "🧅", "Medium size pakka pyaaz"),
            ("Taaza Hara Dhaniya & Mirch Combo", "धनिया + हरी मिर्च", 15, "bundle", "🌿", "Gaddi dhaniya aur 100g teekhi hari mirch"),
            ("Hari Bhindi (Lady Finger)", "ताज़ा भिंडी", 45, "kg", "🌱", "Chhoti naram bina beej wali bhindi"),
            ("Palak Saag (Spinach)", "देसी पालक", 20, "bundle", "🥬", "Khet se tooti hui hari patti"),
            ("Phool Gobhi (Cauliflower)", "फूल गोभी", 30, "piece", "🥦", "Bada safed phool")
        ]
        for name, hname, price, unit, emoji, desc in sabzi_items:
            Product.objects.get_or_create(
                vendor=v1_profile,
                name=name,
                defaults={
                    "hindi_name": hname,
                    "price": price,
                    "unit": unit,
                    "emoji_icon": emoji,
                    "description": desc,
                    "is_available": True
                }
            )

        # Vendor 2: Suresh Fal Bhandar
        v2_user, _ = CustomUser.objects.get_or_create(
            username="vendor_suresh",
            defaults={
                "user_type": "VENDOR",
                "phone": "9899112233",
                "email": "suresh.fal@example.com",
                "first_name": "Suresh",
                "last_name": "Gupta"
            }
        )
        v2_user.set_password("password123")
        v2_user.save()

        v2_profile, _ = VendorProfile.objects.get_or_create(
            user=v2_user,
            defaults={
                "business_name": "Suresh Fresh Fal Thela",
                "category": VendorCategory.FRUITS,
                "phone": "9899112233",
                "upi_id": "sureshfal@okaxis",
                "vehicle_type": VehicleType.CYCLE,
                "city": "New Delhi",
                "area_name": "Janakpuri C-Block & District Centre",
                "pincode": "110058",
                "route_description": "Metro Gate 2 -> C Block Gate 1 -> Mother Dairy Chowk -> Pocket 3 Residents",
                "route_coordinates": json.dumps([
                    [28.6290, 77.0820],
                    [28.6310, 77.0845],
                    [28.6330, 77.0870],
                    [28.6345, 77.0890]
                ]),
                "morning_slot": "8:00 AM - 11:30 AM",
                "evening_slot": "4:00 PM - 8:00 PM",
                "is_active_today": True,
                "status_text": "🍎 Shimla ke taaza seb aur kela ready hain!",
                "is_promoted": True,
                "promotion_plan": "Gali Starter",
                "promotion_expires_at": timezone.now() + timedelta(days=6),
                "rating": 4.8,
                "total_orders": 98
            }
        )

        fruit_items = [
            ("Shimla Red Royal Seb (Apples)", "सेब", 120, "kg", "🍎", "Sweet and crunchy handpicked apples"),
            ("Robusta Kela (Bananas)", "पका केला", 50, "dozen", "🍌", "Fresh yellow ripe bananas"),
            ("Nagpur Santra (Oranges)", "रसीला संतरा", 70, "kg", "🍊", "Juicy sweet seasonal oranges"),
            ("Anar Kandhari (Pomegranate)", "अनार", 140, "kg", "🥭", "Deep red sweet seeds"),
            ("Taaza Papita (Papaya)", "मीठा पपीता", 45, "kg", "🍈", "Naturally ripened papaya")
        ]
        for name, hname, price, unit, emoji, desc in fruit_items:
            Product.objects.get_or_create(
                vendor=v2_profile,
                name=name,
                defaults={
                    "hindi_name": hname,
                    "price": price,
                    "unit": unit,
                    "emoji_icon": emoji,
                    "description": desc,
                    "is_available": True
                }
            )

        # Vendor 3: Ramdas Mitti Ke Bartan
        v3_user, _ = CustomUser.objects.get_or_create(
            username="vendor_ramdas",
            defaults={
                "user_type": "VENDOR",
                "phone": "9871122334",
                "email": "ramdas.pottery@example.com",
                "first_name": "Ramdas",
                "last_name": "Prajapati"
            }
        )
        v3_user.set_password("password123")
        v3_user.save()

        v3_profile, _ = VendorProfile.objects.get_or_create(
            user=v3_user,
            defaults={
                "business_name": "Ramdas Mitti Ke Bartan & Matke",
                "category": VendorCategory.POTTERY,
                "phone": "9871122334",
                "upi_id": "ramdas@paytm",
                "vehicle_type": VehicleType.THELA,
                "city": "New Delhi",
                "area_name": "Janakpuri & Tilak Nagar",
                "pincode": "110058",
                "route_description": "Shani Mandir -> Gali 5 -> Old Post Office lane -> Gurudwara Chowk",
                "route_coordinates": json.dumps([
                    [28.6360, 77.0920],
                    [28.6380, 77.0940],
                    [28.6395, 77.0970]
                ]),
                "morning_slot": "9:00 AM - 1:00 PM",
                "evening_slot": "3:30 PM - 6:30 PM",
                "is_active_today": True,
                "status_text": "🪴 Shuddh mitti ke thande paani wale matke aur handi available!",
                "is_promoted": False,
                "rating": 4.7,
                "total_orders": 53
            }
        )

        pottery_items = [
            ("Lal Mitti Thanda Paani Matka with Tap", "मिट्टी का मटका नल वाला", 180, "piece", "🏺", "Natural terracotta clay water pot, cools water naturally"),
            ("Chai Kulhad Set (Pack of 6)", "मिट्टी के कुल्हड़ (6 पीस)", 60, "bundle", "☕", "Eco-friendly clay tea cups for tandoori chai"),
            ("Mitti ki Handi for Biryani & Dal", "मिट्टी की हांडी", 150, "piece", "🍲", "Safe for stove, authentic desi taste"),
            ("Pooja Clay Diye (Pack of 12)", "मिट्टी के दीये", 40, "packet", "🪔", "Handcrafted clay lamps for daily aarti")
        ]
        for name, hname, price, unit, emoji, desc in pottery_items:
            Product.objects.get_or_create(
                vendor=v3_profile,
                name=name,
                defaults={
                    "hindi_name": hname,
                    "price": price,
                    "unit": unit,
                    "emoji_icon": emoji,
                    "description": desc,
                    "is_available": True
                }
            )

        # Vendor 4: Shyam Ji Phool Wale
        v4_user, _ = CustomUser.objects.get_or_create(
            username="vendor_shyam",
            defaults={
                "user_type": "VENDOR",
                "phone": "9810998877",
                "email": "shyam.phool@example.com",
                "first_name": "Shyam",
                "last_name": "Lal"
            }
        )
        v4_user.set_password("password123")
        v4_user.save()

        v4_profile, _ = VendorProfile.objects.get_or_create(
            user=v4_user,
            defaults={
                "business_name": "Shyam Mandir Phool & Pooja Bhandar",
                "category": VendorCategory.FLOWERS,
                "phone": "9810998877",
                "upi_id": "shyamphool@upi",
                "vehicle_type": VehicleType.CYCLE,
                "city": "New Delhi",
                "area_name": "Janakpuri Mandir Marg & Colony Galis",
                "pincode": "110058",
                "route_description": "Hanuman Mandir lane -> Shiv Mandir -> B-Block Galis 1 to 6 -> Central Park",
                "morning_slot": "6:00 AM - 9:00 AM",
                "evening_slot": "5:30 PM - 7:30 PM",
                "is_active_today": True,
                "status_text": "🌸 Daily Pooja ke taaza genda aur gulab phool ghar-ghar delivery!",
                "is_promoted": False,
                "rating": 4.9,
                "total_orders": 210
            }
        )

        flower_items = [
            ("Pooja Genda Phool Mala (1 Piece)", "गेंदा फूल माला", 30, "piece", "🌼", "Fresh yellow and orange marigold garland"),
            ("Lal Gulab (Red Roses) for Pooja", "लाल गुलाब फूल", 50, "bundle", "🌹", "Pack of fresh fragrant red rose petals"),
            ("Tulsi Patta & Belpatra Packet", "तुलसी और बेलपत्र", 20, "packet", "🍃", "Washed clean leaves for morning pooja")
        ]
        for name, hname, price, unit, emoji, desc in flower_items:
            Product.objects.get_or_create(
                vendor=v4_profile,
                name=name,
                defaults={
                    "hindi_name": hname,
                    "price": price,
                    "unit": unit,
                    "emoji_icon": emoji,
                    "description": desc,
                    "is_available": True
                }
            )

        # 3. Create Sample Scheduled Order
        sample_order, _ = Order.objects.get_or_create(
            order_id="VH-DEMO101",
            defaults={
                "vendor": v1_profile,
                "customer": cust_user,
                "customer_name": "Pooja Sharma",
                "customer_phone": "9876543210",
                "delivery_address": "Flat 204, Shanti Apartments, Gali No. 4",
                "delivery_area": "Janakpuri Block B",
                "delivery_date": timezone.now().date(),
                "delivery_slot": "Morning Round (7:30 AM - 9:00 AM)",
                "payment_method": PaymentMethod.COD,
                "total_amount": 105.00,
                "status": OrderStatus.ACCEPTED,
                "special_instructions": "Please ring bell twice. Ensure tomatoes are ripe."
            }
        )
        if not sample_order.items.exists():
            OrderItem.objects.create(
                order=sample_order,
                product=Product.objects.filter(vendor=v1_profile, name__icontains="Tamatar").first(),
                product_name="Desi Lal Tamatar (Tomato)",
                unit_price=35.0,
                unit="kg",
                quantity=2.0,
                subtotal=70.0
            )
            OrderItem.objects.create(
                order=sample_order,
                product=Product.objects.filter(vendor=v1_profile, name__icontains="Dhaniya").first(),
                product_name="Taaza Hara Dhaniya & Mirch Combo",
                unit_price=15.0,
                unit="bundle",
                quantity=1.0,
                subtotal=15.0
            )
            OrderItem.objects.create(
                order=sample_order,
                product=Product.objects.filter(vendor=v1_profile, name__icontains="Gobhi").first(),
                product_name="Phool Gobhi (Cauliflower)",
                unit_price=20.0,
                unit="piece",
                quantity=1.0,
                subtotal=20.0
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Vendor's Hub database with sample Indian vendors, routes, products, plans, and orders!"))
