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


sitemaps = {
    'posts': PostSitemap,
    'tags': TagSitemap,
}


urlpatterns = i18n_patterns(
    path(_('accounts/login/'), 
         auth_views.LoginView.as_view(template_name='courses/registration/login.html'), 
         name="login"),
    path(_('accounts/logout/'), 
         auth_views.LogoutView.as_view(template_name='courses/registration/logout.html', next_page='/'), 
         name='logout'),
    path('admin/', admin.site.urls),
    path(_('account/'), include('account.urls')),
    path('social-auth/',
         include('social_django.urls', namespace='social')),
    path(_('blog/'), include('blog.urls', namespace='blog')),
    path('sitemap.xml',
         sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap',),
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('course/'), include('courses.urls')),
    path(_('images/'), include('images.urls', namespace='images')),
    path(_('orders/'), include('orders.urls', namespace='orders')),
    path(_('payment/'), include('payment.urls', namespace='payment')),
    path(_('coupons/'), include('coupons.urls', namespace='coupons')),
    path('rosetta/', include('rosetta.urls')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('__debug__/', include('debug_toolbar.urls')),
)

urlpatterns += [
    path(
        'payment/webhook/',
        webhooks.paystack_webhook,
        name='paystack-webhook'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    path('webhook/', webhooks.paystack_webhook, name='paystack-webhook'),
