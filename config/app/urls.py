from rest_framework.routers import DefaultRouter
from django.urls import  path
from .views import ( RestaurantViewSet, CategoryViewSet, MenuItemViewSet,
                    OrderViewSet, OrderItemViewSet, DeliveryViewSet, PaymentViewSet, AddressViewSet)

router = DefaultRouter()
router.register('restaurants/', RestaurantViewSet)
router.register('category/', CategoryViewSet)
router.register('menuitem/', MenuItemViewSet)
router.register('order/', OrderViewSet)
router.register('orderitem/', OrderItemViewSet)
router.register('delivery/', DeliveryViewSet)
router.register('payment/', PaymentViewSet)
router.register('address/', AddressViewSet)

urlpatterns = router.urls
