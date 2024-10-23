# Educa - Integrated Learning & Social Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Educa is a comprehensive Django-based platform that combines an eLearning app with a blog, shop and social platform. _(from the book, Django By Example)_

## ✨ Core Features

### 🎓 eLearning Platform
- Course creation and management
- Multiple content types support (text, video, files)
- Student enrollment and progress tracking
- Interactive course discussion forums
- Real-time chat functionality for students and instructors
![alt-text](demo/elearing-screenshot.jpg)

### 📝 Blog System
- Multi-author blog support
- Advanced tagging system
- RSS feeds
- Similar posts suggestions
- Markdown support for posts
- Comment system with threading
- Post sharing via email
![alt-text](demo/blog-screenshot.jpg)

### 📌 Social Bookmarking
- Image bookmarking from any website
- Custom bookmarklet for easy saving
- AJAX-powered infinite scroll
- Social following system
- Activity stream for users
- Image likes and favorites
![alt-text](demo/social-screenshot.jpg)

### 🛍️ Online Shop
- Product catalog with categories
- Shopping cart using Django sessions
- Order management system
- Payment integration (Stripe/PayPal)
- PDF invoice generation
- Product recommendations
- Digital product delivery
![alt-text](demo/shop-screenshot.jpg)

## 🚀 Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- Redis
- RabbitMQ/Redis (for Celery)
- Pillow dependencies for image processing

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/jjokah/educa.git
cd educa
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
touch .env
# Edit .env file with your settings
```
Key settings in `.env`:

```plaintext
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/educa
REDIS_URL=redis://localhost:6379
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
```

5. Initialize the database:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata initial_data.json
```

6. Start services:
```bash
redis-server
celery -A educa worker -l info
python manage.py runserver
```

## 🏗️ System Architecture

### Applications Structure
```
educa/
├── courses/        # App for managing courses
├── blog/           # Blog system
├── action/         # Tracking user activities
├── cart/           # Shopping cart functionalities
├── images/         # Social bookmarking
├── shop/           # Online shop
├── accounts/       # User management
├── chat/           # Real-time messaging
├── templates/      # HTML templates for the frontend
├── static/         # Static assets (CSS, JS, images)
├── educa/          # Main project dir (settings, URLs, etc)
└── common/         # Shared utilities

```

### Functional Overview

**Blog**
![alt-text](./demo/blog-func.jpg)

**Social**
![alt-text](./demo/social-func1.jpg)
![alt-text](./demo/social-func2.jpg)

**Shop**
![alt-text](./demo/shop-func1.jpg)
![alt-text](./demo/shop-func2.jpg)

**eLearning**
![alt-text](./demo/elearning-func1.jpg)
![alt-text](./demo/elearning-func2.jpg)


### Key Technologies

- **Frontend**:
  - JavaScript/jQuery
  - AJAX for dynamic loading
  - WebSockets for real-time features
  - Custom bookmarklet
  - Bootstrap

- **Backend**:
  - Django
  - Django Channels
  - Django REST framework
  - Celery
  - Redis
  - PostgreSQL

- **Additional Tools**:
  - Pillow for image processing
  - WeasyPrint for PDF generation
  - django-taggit for tagging
  - Easy-thumbnails for image thumbnails




## 🚀 Deployment

Deployment instructions for production (PythonAnywhere):

1. Set up server with required dependencies
2. Configure nginx/gunicorn
3. Set up SSL certificates
4. Configure PostgreSQL
5. Set up Redis and Celery
6. Configure static/media files serving
7. Set environment variables
