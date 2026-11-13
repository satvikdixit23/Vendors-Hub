from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('VENDOR', 'Vendor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='CUSTOMER')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True, help_text="Default house/gali address")
    firebase_uid = models.CharField(max_length=128, unique=True, blank=True, null=True)

    def is_vendor(self):
        return self.user_type == 'VENDOR'

    def is_customer(self):
        return self.user_type == 'CUSTOMER'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

