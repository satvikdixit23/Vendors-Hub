import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
from django.contrib.auth import get_user_model

class FirebaseAuthMiddleware:
    """Middleware that verifies a Firebase ID token (if present) and
    authenticates the corresponding Django ``CustomUser``.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self._initialize_firebase()

    def _initialize_firebase(self):
        # Initialize the Firebase Admin SDK only once.
        if not firebase_admin._apps:
            cred_path = getattr(settings, "FIREBASE_CERT_PATH", None)
            if cred_path:
                cred = credentials.Certificate(str(cred_path))
                firebase_admin.initialize_app(cred)
            else:
                # If path missing, raise a clear error during dev.
                raise RuntimeError("FIREBASE_CERT_PATH is not set in settings.")

    def __call__(self, request):
        # Expect token in Authorization header as "Bearer <idToken>".
        header = request.META.get("HTTP_AUTHORIZATION", "")
        if header.startswith("Bearer "):
            id_token = header.split("Bearer ", 1)[1]
            try:
                decoded = auth.verify_id_token(id_token)
                uid = decoded.get("uid")
                if uid:
                    User = get_user_model()
                    try:
                        user = User.objects.get(firebase_uid=uid)
                        request.user = user
                    except User.DoesNotExist:
                        # No matching user – leave request.user as Anonymous.
                        pass
            except Exception as e:
                # Invalid token – ignore and continue as anonymous.
                pass
        return self.get_response(request)
