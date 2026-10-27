# DermaVisionAI 🌿
### Intelligent Skin Analysis & Personalized Skincare Guidance

**DermaVisionAI** is a state-of-the-art AI-powered web application that analyzes a user's facial image captured through a camera or uploaded from their device. It identifies the user's **skin type** (Oily, Dry, Normal, Combination) and **common skin concerns** (Acne, Hyperpigmentation, Dark Spots, Redness, Texture/Pores), generating tailored dermatological skincare routines and budget-matched product recommendations in Indian Rupees (₹).

---

## 🌟 Key Features

* 📷 **Dual Image Acquisition**: In-browser live camera capture via WebRTC (`getUserMedia`) with facial alignment oval guide, or high-res file upload (JPG, PNG, WebP) with drag-and-drop.
* 🤖 **AI & Computer Vision Analysis**:
  * Face detection and ROI localization (Forehead, T-Zone, Cheeks, Chin) via OpenCV Haar Cascades.
  * Multi-spectrum skin segmentation using YCrCb and HSV color spaces.
  * Specular highlight and sebum shine ratio analysis.
  * Erythema and red blemish contour detection (LAB $a^*$ channel).
  * Melanin and hyperpigmentation contrast mapping (LAB $L^*$ and $b^*$ channels).
  * Laplacian variance texture and pore density evaluation.
* 🧠 **Deep Learning CNN**: TensorFlow / Keras Convolutional Neural Network classifying skin patterns with consensus weighting.
* 🔍 **Visual Diagnostic Overlay**: High-tech annotated output displaying face boundaries, neon red markers on acne lesions, amber boxes on dark spots, and a clinical HUD bar.
* 💰 **Smart Budget Selector (₹)**: Quick buttons (₹500, ₹1000, ₹1500, ₹2500, ₹4000+) or custom INR input with real-time dynamic recalculation without page reload.
* 🧴 **Budget-Based Skincare Recommendations**: Curated database of active-ingredient products (Salicylic Acid, Niacinamide, Ceramides, Vitamin C, Hyaluronic Acid, etc.) matched to the user's budget and skin concerns.
* 📅 **Structured Morning & Night Routines**: Step-by-step AM/PM schedules with application instructions and dermatologist pro-tips.
* 🛒 **Integrated E-Commerce Cart**: Add recommended products individually or add the entire routine with a single click, quantity adjuster, and free shipping tracker.
* 📦 **Delivery Address Management**: Complete Indian address handling (Flat/Building, Street, City, State, PIN code) with multi-address saving for 1-click checkout.
* 💳 **Multi-Option Online Payment Gateway**: Simulated payment gateway supporting UPI (GPay, PhonePe, Paytm with VPA verification & QR code), Credit/Debit Cards (with 2FA banking animation), Net Banking, and Cash on Delivery.
* 📋 **Order Confirmation & Digital Invoices**: Order ID generation, real-time shipment milestone progress stepper, and print-ready tax invoice receipts.
* 👤 **User Authentication & History**: Secure user registration, login, profile management, persistent scan history, and complete order history.
* 🗄️ **Dual Database Architecture**: Direct support for MySQL / phpMyAdmin with seamless zero-config SQLite fallback.
* 🖨️ **Printable Report & Invoice**: Clean CSS print styling for saving or printing personal skin reports and tax invoices.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons, WebRTC API |
| **Backend** | Python Flask, Werkzeug (Security & Password Hashing), Jinja2 |
| **AI & Computer Vision** | OpenCV 4.x, TensorFlow 2.x, Keras 3.x, NumPy, SciPy, Scikit-learn, Pillow |
| **Database** | MySQL / phpMyAdmin (`dermavision_db`), SQLite (`dermavision.db` fallback) |
| **Development Tool** | VS Code / Python 3.13 |

---

## 📂 Project Directory Structure

```text
DermaVisionAI/
├── app.py                      # Flask main application & API controllers
├── config.py                   # App configuration & database parameters
├── database.py                 # Dual database manager (MySQL & SQLite fallback)
├── ai_engine.py                # OpenCV multi-spectrum skin analysis & HUD overlays
├── skin_model.py               # Deep Learning CNN architecture (TensorFlow/Keras)
├── products_data.py            # Skincare product catalog, routines & budget engine
├── schema.sql                  # Full SQL database schema & seed products for MySQL
├── requirements.txt            # Python dependencies
├── generate_test_samples.py    # Generates realistic synthetic face test images
├── test_app.py                 # Automated unit and integration test suite
├── static/
│   ├── css/
│   │   └── style.css           # Dermatology clinic aesthetic & responsive design
│   ├── js/
│   │   └── main.js             # Camera capture, drag & drop, dynamic AJAX budget
│   ├── samples/                # Sample test face images
│   └── uploads/                # User uploads and annotated diagnostic overlays
└── templates/
    ├── base.html               # Master layout with navbar, alerts & disclaimer
    ├── index.html              # Landing page with workflow & skin type guide
    ├── analyze.html            # Camera capture, file upload & budget selector
    ├── results.html            # Diagnostic overlay, biomarkers, products & routines
    ├── history.html            # Past skin reports & progression timeline
    ├── products.html           # Skincare product catalog with multi-filters
    ├── login.html              # User login
    ├── register.html           # User registration
    ├── profile.html            # User profile overview
    └── about.html              # System architecture, limitations & future scope
```

---

## 🚀 How to Run the Application

### 1. Prerequisites
Ensure Python 3.10+ (or Python 3.13) is installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup Options

#### Option A: Automatic SQLite (Zero-Config, Runs Instantly)
The application will automatically initialize `dermavision.db` with all tables and seed data if MySQL is not detected. No manual configuration is required!

#### Option B: MySQL / phpMyAdmin (XAMPP / WAMP)
1. Start **Apache** and **MySQL** in XAMPP or WAMP control panel.
2. Open phpMyAdmin at `http://localhost/phpmyadmin`.
3. Create a database named `dermavision_db` (or simply import `schema.sql` directly).
4. Run the SQL queries in `schema.sql` to create the tables and seed products.
5. In `config.py` (or via environment variables), set:
   ```python
   DB_TYPE = 'mysql'
   MYSQL_HOST = 'localhost'
   MYSQL_PORT = 3306
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = '' # Your MySQL password
   MYSQL_DB = 'dermavision_db'
   ```

### 4. Run the Flask Web Application
```bash
python app.py
```
Open your browser and visit: **`http://127.0.0.1:5000`**

### 5. Run the Automated Tests
```bash
python test_app.py
```

---

## 🧪 Testing Without a Camera
If you do not have a live webcam available, you can use the pre-generated sample face images located in:
`static/samples/sample_combination_acne.jpg`
`static/samples/sample_oily_skin.jpg`
`static/samples/sample_dry_normal.jpg`

Simply upload one of these images on the **AI Skin Scan** page to see the real-time biomarker extraction, acne/melanin detection, and diagnostic overlay in action.

---

## ⚠️ Medical Disclaimer
> **IMPORTANT:** DermaVisionAI provides **general skincare guidance only**. It is **not a medical diagnostic system** and does not replace consultation with a qualified dermatologist. Users experiencing persistent or severe dermatological symptoms should consult a healthcare professional.

---

## 🔮 Future Scope
* **Mobile Application**: Cross-platform iOS and Android mobile app.
* **Continuous AI Training**: Larger multi-ethnic dermatological datasets.
* **Real-time Video Analysis**: 60fps face mesh tracking for instant live recommendations.
* **Tele-Dermatology**: Direct consultation booking with licensed dermatologists.
* **Multilingual Support**: Hindi, Bengali, Tamil, Telugu, and other regional languages.
* **Skin Progress Tracker**: Longitudinal timeline tracking acne recovery and moisture improvements.
