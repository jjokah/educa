# Educa - Integrated Learning & Social Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Educa is a comprehensive Django-based project integrating an eLearning platform with a blog system, an online shop and a social platform. 

## ✨ Core Features

### 🎓 eLearning Platform
- Course creation and management
- Multiple content types support (text, video, files)
- Student enrollment and progress tracking
- Interactive course discussion forums
- Real-time chat functionality for students and instructors
![alt-text](./demo/elearing-screenshot.jpg)

### 📝 Blog System
- Multi-author blog support
- Advanced tagging system
- RSS feeds
- Similar posts suggestions
- Markdown support for posts
- Comment system with threading
- Post sharing via email
![alt-text](./demo/blog-screenshot.jpg)

### 📌 Social Bookmarking
- Image bookmarking from any website
- Custom bookmarklet for easy saving
- AJAX-powered infinite scroll
- Social following system
- Activity stream for users
- Image likes and favorites
![alt-text](./demo/social-screenshot.jpg)

### 🛍️ Online Shop
- Product catalog with categories
- Shopping cart using Django sessions
- Order management system
- Payment integration (Stripe/PayPal)
- PDF invoice generation
- Product recommendations
- Digital product delivery
![alt-text](./demo/shop-screenshot.jpg)

## 🚀 Installation

### Prerequisites
- Python 3.10+
- [PostgreSQL](https://www.postgresql.org/download/) (database)
- [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) (caching)
- [RabbitMQ](https://www.rabbitmq.com/docs/download) (async)
- [WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation) (pdf)

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
REDIS_HOST=localhost
REDIS_POST=6379
REDIS_DB=0
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

**Blog:**
- _post list, post details_
- _pagination, post comments, email sharing_
- _tagging, markdown, sitemap, RSS feed, search engine_
![alt-text](./demo/blog-func.jpg)

**Social:**
- _user account_
- _social authentication_
- _bookmarking, liking, infinite scroll_
- _track user actions_
![alt-text](./demo/social-func1.jpg)
![alt-text](./demo/social-func2.jpg)

**Shop:**
- _product listing, shopping cart, order creation_
- _ordering management, payment integration_
- _coupon system, recommendation engine_
- _internationalization_
![alt-text](./demo/shop-func1.jpg)
![alt-text](./demo/shop-func2.jpg)

**E-Learning:**
- _content management system_
- _rendering and caching content_
- _API views and end points_
- _chat server_
![alt-text](./demo/elearning-func1.jpg)
![alt-text](./demo/elearning-func2.jpg)


### Key Technologies

- **Frontend**:
  - HTML/CSS
  - JavaScript/jQuery
  - AJAX for dynamic loading
  - Custom bookmarklet

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
  - WebSockets for real-time features
  - django-taggit for tagging
  - Easy-thumbnails for image thumbnails




## 🚀 Deployment

Deployment instructions for production:

1. Set up server with required dependencies
2. Configure nginx/gunicorn
3. Set up SSL certificates
4. Configure PostgreSQL
5. Set up Redis and Celery
6. Configure static/media files serving
7. Set environment variables

## Acknowledgement
Thanks to the **Antonio Melé** for his book, _**Django By Example** which this project is based on._