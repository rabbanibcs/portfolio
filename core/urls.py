
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from portfolio.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name="portfolio-index"),
    path('portfolio/', include('portfolio.urls')),
    path('blog/',include('blog.urls')),
    path('shop/',include('ecommerce.urls')),
    path('user/',include('user.urls')),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)