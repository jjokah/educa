from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from blog.sitemaps import PostSitemap, TagSitemap
from payment import webhooks


# Register sitemaps for blog posts and tags
sitemaps = {
    'posts': PostSitemap,
    'tags': TagSitemap,
}

# Main URL patterns
urlpatterns = [
    # Utility routes 
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('payment/webhook/', webhooks.paystack_webhook, name='paystack-webhook'),

    # API endpoints for e-learning platform
    path('api/', include('courses.api.urls', namespace='api')),

    # SEO and site navigation
    path('sitemap.xml',
         sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap',),

    # Authentication routes
    path('accounts/login/', 
         auth_views.LoginView.as_view(template_name='courses/registration/login.html'), 
         name="login"),
    path('accounts/logout/', 
         auth_views.LogoutView.as_view(template_name='courses/registration/logout.html', next_page='/'), 
         name='logout'),
    path('account/', include('account.urls')),
    path('social-auth/',
         include('social_django.urls', namespace='social')),
    
    # Application routes
    path('blog/', include('blog.urls', namespace='blog')),
    path('course/', include('courses.urls')),
    path('images/', include('images.urls', namespace='images')),
    path('students/', include('students.urls')),
]

# Internationalized URL patterns for e-commerce
urlpatterns += i18n_patterns(
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('orders/'), include('orders.urls', namespace='orders')),
    path(_('payment/'), include('payment.urls', namespace='payment')),
    path(_('coupons/'), include('coupons.urls', namespace='coupons')),
    path('shop/', include('shop.urls', namespace='shop')),
)

# Debug route
urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Use webhook/ route in development
    path('webhook/', webhooks.paystack_webhook, name='paystack-webhook'),
