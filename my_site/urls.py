from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_shop import views
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'dishes', views.DishViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include('rest_shop.urls')),
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('', include('social_django.urls', namespace='social'))
]
if settings.DEBUG:
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





