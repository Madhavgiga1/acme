from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, WebhookViewSet, index

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'webhooks', WebhookViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
]