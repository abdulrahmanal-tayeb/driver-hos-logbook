# 🚛 Driver HOS Logbook: HOS-Compliant Smart Routing & ELD Logbook

![Django](https://img.shields.io/badge/Django-5.2+-092e20?style=for-the-badge&logo=django&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16+-000000?style=for-the-badge&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-19+-61dafb?style=for-the-badge&logo=react&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.0-38b2ac?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-1.9-199900?style=for-the-badge&logo=leaflet&logoColor=white)

**Driver HOS Logbook** is a sophisticated full-stack application designed for property-carrying commercial drivers to plan routes while maintaining strict adherence to **Hours of Service (HOS)** regulations. It intelligently calculates driving segments, inserts mandated rest breaks, and generates audit-ready Daily Log Sheets.

---

> [!NOTE]
> The hosted version of this application may experience delays (30-60 seconds) on initial requests due to **cold starts** on the free hosting plan.

---

## 🌟 Key Features

- **Smart Routing Engine**: Calculates optimal routes using OSRM, integrated with real-world geocoding.
- **HOS Compliance Automation**:
    - **11-Hour Driving Limit**: Automatically caps driving segments and inserts breaks.
    - **14-Hour Duty Limit**: Tracks total on-duty time including inspections and loading.
    - **30-Minute Break Rule**: Inserts rest breaks after 8 hours of cumulative driving.
    - **70-Hour/8nd-Day Rule**: Manages long-term cycle compliance with 34-hour restart logic.
    - **10-Hour Rest Requirement**: Schedules mandatory daily rest periods.
- **Logbook Automation**: Generates multi-day ELD log sheets from calculated trips.
- **Smart Stop Integration**:
    - Automatic 1-hour loading/unloading stops at pickup and drop-off.
    - Fuel stop optimization (every 1,000 miles).
- **Interactive Visualization**: Real-time map rendering with route geometry and stop markers.

---

## 🛠️ Technical Architecture

### **Backend (Django & DRF)**
Built with a focus on **Clean Architecture** and **Maintainability**:
- **Fat Serializer Pattern**: Business logic for HOS calculation and persistence is encapsulated in serializers, keeping views thin and testable.
- **Transactional Integrity**: Uses `transaction.atomic` to ensure atomic updates of Trips, LogEntries, and RouteStops.
- **Mocked Integration Tests**: Comprehensive test suite with network call mocking for reliable verification.
- **Dynamic Configuration**: Powered by `django-configurations` for environment-specific settings.

### **Frontend (Next.js & React)**
A modern, premium UI/UX experience:
- **Next.js 16 (App Router)**: Utilizing React 19's latest features for high performance.
- **Tailwind CSS 4**: Cutting-edge styling with rich aesthetics and responsive design.
- **Leaflet.js**: High-performance interactive map integration.
- **Type-Safe**: Full TypeScript implementation for robust frontend logic.

---

## 🚀 Getting Started

### **Prerequisites**
- Python 3.12+
- Node.js 20+
- Poetry (for backend dependency management)

### **Backend Setup**
1. Navigate to the `be/driver_hos_logbook` directory.
2. Install dependencies: `poetry install`
3. Set up environment variables: Copy `dev.env` to `.env`.
4. Run migrations: `poetry run python manage.py migrate`
5. Start the server: `poetry run python manage.py runserver`

### **Frontend Setup**
1. Navigate to the `fe/driver_hos_logbook` directory.
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

---

## 📊 API Documentation

The backend is fully documented with **OpenAPI 3.0** schemas. You can access the interactive documentation at the following endpoints:
- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`
- **OpenAPI Schema**: `/api/schema/`

---

## ✅ Assessment Requirements Mapping
- [x] **Full-stack App**: Django + React implementation.
- [x] **Core Logic**: Takes trip details and outputs route + ELD logs.
- [x] **Map Integration**: Free Map API (OSRM + Leaflet) used.
- [x] **Daily Log Sheets**: Automated generation for multi-day trips.
- [x] **HOS Rules**: Implemented 11h/14h/30min/70h rules.
- [x] **Assumption Handling**: 1000-mile fuel stops, 1h loading/unloading stops.
