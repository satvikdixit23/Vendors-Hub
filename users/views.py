from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import CustomUser
from vendors.models import VendorProfile, VendorCategory, VehicleType

def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'vendor_profile'):
            return redirect('vendor_dashboard')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if hasattr(user, 'vendor_profile'):
                return redirect('vendor_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'users/login.html')

def demo_login_view(request, role):
    """1-Click quick login for testing as vendor or customer"""
    if role == 'vendor':
        user = CustomUser.objects.filter(username='vendor_ramesh').first()
        if user:
            login(request, user)
            messages.success(request, "Logged in as Demo Vendor (Ramesh Sabziwala)!")
            return redirect('vendor_dashboard')
    elif role == 'customer':
        user = CustomUser.objects.filter(username='customer_pooja').first()
        if user:
            login(request, user)
            messages.success(request, "Logged in as Demo Customer (Pooja Sharma)!")
            return redirect('home')
    messages.error(request, "Demo account not found. Please run seed data.")
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user_type = request.POST.get('user_type', 'CUSTOMER')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        full_name = request.POST.get('full_name', '')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'users/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose another.")
            return render(request, 'users/register.html')

        # Create user
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            user_type=user_type
        )

        if user_type == 'VENDOR':
            business_name = request.POST.get('business_name', f"{full_name}'s Cart")
            category = request.POST.get('category', VendorCategory.SABZI)
            area_name = request.POST.get('area_name', 'Local Colony')
            city = request.POST.get('city', 'New Delhi')
            route_desc = request.POST.get('route_description', 'Daily rounds in local streets')
            vehicle = request.POST.get('vehicle_type', VehicleType.THELA)

            VendorProfile.objects.create(
                user=user,
                business_name=business_name,
                category=category,
                phone=phone,
                city=city,
                area_name=area_name,
                route_description=route_desc,
                vehicle_type=vehicle
            )
            login(request, user)
            messages.success(request, f"Vendor account created! Welcome {business_name}.")
            return redirect('vendor_dashboard')
        else:
            login(request, user)
            messages.success(request, f"Welcome to Vendor's Hub, {full_name}!")
            return redirect('home')

    return render(request, 'users/register.html', {
        'categories': VendorCategory.choices,
        'vehicles': VehicleType.choices
    })

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
