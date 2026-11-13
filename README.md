# 🛒 Vendor's Hub (फेरीवाला / ठेला संगम)

[![Django](https://img.shields.io/badge/Django-5.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Leaflet](https://img.shields.io/badge/Leaflet-Map-199900?style=for-the-badge&logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![Razorpay](https://img.shields.io/badge/Razorpay-Integrated-0C2340?style=for-the-badge&logo=razorpay&logoColor=white)](https://razorpay.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Empowering Local Street Vendors (ठेलेवाले / फेरीवाले) with Hyperlocal Live Route Tracking, Doorstep Pre-Orders, and Zero Platform Commission.**

---

## 📌 Problem Statement & Vision

In Indian cities and mohallas, traditional street carts (**Thelas**) supply fresh vegetables, seasonal fruits, clay pottery, fresh flowers, and morning newspapers directly to residents' doorsteps at authentic mandi prices. However:

1. **Lack of Predictability**: Residents never know the exact time a thela will pass through their gali.
2. **Loss of Livelihood**: Heavy venture-backed dark-store apps charge steep markups and crush independent street vendors.
3. **No Direct Pre-Orders**: Customers cannot reserve specific items in advance before the thela sells out.

**Vendor's Hub** bridges this gap by giving local vendors a digital storefront and route schedule while preserving their traditional door-to-door street commerce with **0% commission** and **100% direct cash/UPI payments**.

---

## ⚡ Key Features

### 🗺️ 1. Interactive Neighborhood Route Tracker
- **Real-Time Colony Maps**: Built with Leaflet.js and high-performance CartoDB Voyager tiles.
- **Custom Emojis & Pins**: Instant visual distinction between Sabzi (🥦), Fruits (🍎), Pottery (🏺), Flowers (🌸), and Newspapers (🗞️).
- **Featured Vendor Highlights**: Gold glow badges and priority map placement for boosted thelas.
- **Colony Route Paths**: Shows operational rounds and neighborhood gali stops.

### 🛍️ 2. Quick-Commerce (Zepto / Blinkit Style) Storefront
- **Modern UI & High-Contrast Cards**: Designed with Plus Jakarta Sans typography and vibrant emerald & amber accents.
- **Dynamic Quantity Stepper**: Seamless `+ ADD` button that morphs into a reactive `[ - ] [ QTY ] [ + ]` selector.
- **Mobile Floating Cart Bar**: Bottom drawer showing active basket items and total amount.
- **Bilingual Items**: English product titles paired with local Hindi names (e.g., *Fresh Red Tomatoes / देशी लाल टमाटर*).

### ⏰ 3. Doorstep Pre-Orders & Route Slots
- **Morning & Evening Rounds**: Choose convenient delivery slots (e.g., `7:00 AM - 11:30 AM` or `4:30 PM - 8:30 PM`).
- **Zero Risk / Zero Prepayment**: Customers pay in cash (COD) or scan the vendor's own UPI QR code upon arrival.
- **Live Order Timeline**: 3-step progress tracker (`Reserved` ➔ `On Route` ➔ `Delivered`).
- **Direct WhatsApp & Phone Connect**: 1-click button to chat with or call the vendor directly.

### 🥦 4. Comprehensive Vendor Partner Console
- **Live Status Toggle**: Toggle between `🟢 Live On Route` and `⚪ Thela Closed` with a real-time status ticker (e.g., *"Near Gali 4, fresh apples just arrived!"*).
- **1-Click Auto-Stock**: Automatically populate category-specific inventory presets in seconds.
- **Route Manager**: Interactive visualizer to set mohalla stops, landmarks, and operational hours.
- **Customer Order Hub**: Real-time incoming pre-orders with instant status updater.
- **Promotions & Boost**: Tiered visibility plans (*Gali Starter*, *Mohalla Star*, *City Booster*) integrated with Razorpay.

### ⚡ 5. 1-Click Instant Demo Access
- Quick login buttons on the sign-in page to instantly test the platform as either:
  - **Vendor**: *Ramesh Kumar (Ramesh Desi Sabzi Bhandar)*
  - **Customer**: *Pooja Sharma (Janakpuri Resident)*

---

## 🏗️ Architecture & Tech Stack

```
Vendor's Hub
│
├── core/                # Core discovery, homepage, search, & context processors
│   └── management/      # Database seeding scripts (seed_data.py)
├── users/               # Custom user model (Customer vs. Vendor), authentication
├── vendors/             # Vendor profiles, storefront, products, route manager, promotions
├── orders/              # Pre-order placement, checkout logic, item tracking
├── payments/            # Razorpay integration & webhook handlers
├── templates/           # Clean, modular Tailwind HTML templates
│   ├── core/            # Homepage with Leaflet route map & thela discovery
│   ├── vendors/         # Storefront, partner dashboard, product/route managers
│   ├── orders/          # Checkout, order tracking, order history
│   └── users/           # Modern authentication & registration
└── static/              # Static styling & client assets
```

| Layer | Technology |
|---|---|
| **Framework** | Django 5.2+ (Python 3.12+) |
| **Frontend Styling** | Tailwind CSS (CDN / JIT), Plus Jakarta Sans |
| **Interactive Maps** | Leaflet.js + CartoDB Voyager Raster Tiles |
| **Database** | SQLite (development) / PostgreSQL ready |
| **Payments** | Razorpay SDK (Test/Live gateway support) |
| **Communication** | Direct WhatsApp API links & tel: integrations |

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/satvikdixit23/Vendors-Hub.git
cd Vendors-Hub
```

### 2. Create and Activate Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the sample environment file:
```bash
cp .env.example .env
```
*(Optional: customize `SECRET_KEY`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` in `.env`)*

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Seed Realistic Demo Data
Populate realistic Indian street vendors, neighborhoods, routes, products, and promotion plans:
```bash
python manage.py seed_data
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to **`http://127.0.0.1:8000/`**.

---

## 🔑 Demo Credentials

| Role | Username | Password | Notes |
|---|---|---|---|
| **Vendor** | `vendor_ramesh` | `ramesh123` | Desi Sabzi Thelawala (Janakpuri Block B) |
| **Customer** | `customer_pooja` | `pooja123` | Colony Resident with past orders |
| **Super Admin** | `admin` | `admin123` | Access to `/admin/` management portal |

*(You can also use the **1-Click Instant Demo Login** buttons on the `/auth/login/` page!)*

---

## 📱 Mobile-First Responsive Design

- **Sticky Mobile Bottom Navigation**: Quick tabs for Home, Thelas, Orders, and Profile.
- **Touch-Friendly Tap Targets**: Sized for quick single-handed thumb interaction.
- **Optimized Map Gestures**: Smooth zooming, custom emoji markers, and fast rendering.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Satvik Dixit**
- GitHub: [@satvikdixit23](https://github.com/satvikdixit23)
- Email: [2501640130060@psit.ac.in](mailto:2501640130060@psit.ac.in)

---
*Empowering India's street vendors with zero commission and modern hyperlocal technology.* 🇮🇳
