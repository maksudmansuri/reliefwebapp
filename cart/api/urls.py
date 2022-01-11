from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'cart', views.CartViewSet)
router.register(r'delivery-cost', views.DeliveryCostViewSet)
# router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include((router.urls, 'eca.cart'))),
]