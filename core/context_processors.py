from django.conf import settings

def settings_context(request):
    return {
        'settings': {
            'MAPS_API_KEY': getattr(settings, 'MAPS_API_KEY', ''),
            'RAZORPAY_KEY_ID': getattr(settings, 'RAZORPAY_KEY_ID', ''),
        }
    }
