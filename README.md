# 🏠 RENTIFY — Peer-to-Peer Item Rental Marketplace

A full-stack web application built with Django that lets users list personal items for rent, browse available items, request rentals, and pay through Razorpay (test mode).

## Notes
- Payments run in Razorpay test mode. Use Razorpay's test cards.
- Not deployed. Clone the repo and run it locally using the steps below.

## ✨ Features

- **User Authentication** — Signup, login, logout with input validation
- **User Profiles** — Profile management with profile pictures
- **Item Management** — List, edit, and delete items with categories, conditions, and images
- **Rental Workflow** — Request → Approve/Reject → Payment → Ongoing → Completed
- **Razorpay Payments** — Integrated payment gateway for secure transactions
- **Wishlist** — Save items for later
- **Reviews & Ratings** — Rate and review items after rental
- **Disputes** — Raise and manage rental disputes
- **Notifications** — In-app notification system for rental updates
- **Admin Panel** — Full admin dashboard for managing users, items, and transactions

## 🛠️ Tech Stack

- **Backend:** Python 3.13, Django 5.2
- **Database:** SQLite (development) 
- **Payments:** Razorpay (Test Mode)
- **Frontend:** Django Templates, Bootstrap 5, CSS3
- **Authentication:** Django Auth

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rentify.git
   cd rentify
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv myenv

   # Windows
   myenv\Scripts\activate

   # macOS/Linux
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `myproject/` directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   RAZORPAY_KEY_ID=your-razorpay-key
   RAZORPAY_KEY_SECRET=your-razorpay-secret
   ```

5. **Run migrations:**
   ```bash
   cd myproject
   python manage.py migrate
   ```

6. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Open in browser:**
   - App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 📁 Project Structure

```
myproject/
├── authen/          # User authentication (signup, login, password)
├── base/            # Core app (items, rentals, reviews, disputes)
├── payments/        # Razorpay payment integration
├── templates/       # Shared templates (navbar, footer, base)
├── static/          # CSS, JavaScript
├── media/           # User uploaded files
├── manage.py
└── myproject/       # Django project settings
```

## 📸 Screenshots

> _Add screenshots of your application here_

## 📄 License

This project is for educational purposes.
