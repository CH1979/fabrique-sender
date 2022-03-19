from rest_framework import routers

from .views import CustomerViewSet, MaillistViewSet


router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
urlpatterns = router.urls
