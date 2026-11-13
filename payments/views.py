import json
import hmac
import hashlib
from datetime import timedelta

from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from vendors.models import PromotionPlan, VendorProfile

try:
    import razorpay
except ImportError:
    razorpay = None

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)) if razorpay else None


def checkout_view(request, plan_id):
    """Create a Razorpay order and return JSON for the frontend."""
    plan = get_object_or_404(PromotionPlan, id=plan_id)
    if not client:
        return JsonResponse({"error": "Razorpay SDK not installed"}, status=500)

    vendor_id = 0
    if request.user.is_authenticated and hasattr(request.user, 'vendor_profile'):
        vendor_id = request.user.vendor_profile.id

    amount = int(plan.price * 100)
    data = {
        "amount": amount,
        "currency": "INR",
        "receipt": f"promotion_{plan.id}_{vendor_id}",
        "payment_capture": 1,
    }
    razorpay_order = client.order.create(data=data)
    response = {
        "order_id": razorpay_order["id"],
        "amount": amount,
        "currency": "INR",
        "key_id": settings.RAZORPAY_KEY_ID,
        "plan_id": plan.id,
        "description": plan.name,
    }
    return JsonResponse(response)

@csrf_exempt
def payment_webhook(request):
    """Handle Razorpay webhook, verify signature, and activate promotion."""
    payload = request.body
    received_sig = request.META.get('HTTP_X_RAZORPAY_SIGNATURE', '')
    generated_sig = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(received_sig, generated_sig):
        return HttpResponseBadRequest('Invalid signature')

    event = json.loads(payload)
    if event.get('event') == 'payment.captured':
        payment_entity = event['payload']['payment']['entity']
        receipt = payment_entity.get('receipt', '')
        try:
            _, plan_id, vendor_id = receipt.split('_', 2)
            plan = PromotionPlan.objects.get(id=plan_id)
            vendor = VendorProfile.objects.get(id=vendor_id)
            vendor.is_promoted = True
            vendor.promotion_plan = plan.name
            vendor.promotion_expires_at = timezone.now() + timedelta(days=plan.duration_days)
            vendor.save()
        except (ValueError, PromotionPlan.DoesNotExist, VendorProfile.DoesNotExist):
            pass
    return JsonResponse({'status': 'ok'})
