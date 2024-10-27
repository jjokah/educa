from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.sitemaps import PostSitemap, TagSitemap


sitemaps = {
    'posts': PostSitemap,
    'tags': TagSitemap,
}


urlpatterns = [
    path("accounts/login/", 
         auth_views.LoginView.as_view(template_name='courses/registration/login.html'), 
         name="login"
    ),
    path("accounts/logout/", 
         auth_views.LogoutView.as_view(template_name='courses/registration/logout.html', next_page='/'), 
         name="logout"
    ),
    path("admin/", admin.site.urls),
    path('account/', include('account.urls')),
    path(
        'social-auth/',
        include('social_django.urls', namespace='social')
    ),
    path('blog/', include('blog.urls', namespace='blog')),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
    path('cart/', include('cart.urls', namespace='cart')),
    path('course/', include('courses.urls')),
    path('images/', include('images.urls', namespace='images')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
