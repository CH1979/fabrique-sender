from django.urls import path
from rest_framework import routers

from sender.views import (
    CustomerViewSet,
    MaillistViewSet,
    MaillistListAPIView,
)


urlpatterns = [
    path(r'maillists/', MaillistListAPIView.as_view(), name='maillists'),
]
router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'maillist', MaillistViewSet, basename='maillist')

urlpatterns += router.urls
