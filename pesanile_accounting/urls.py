from django.urls import path
from .views import ServicePaymentAPIView

urlpatterns = [
    path('service-payment/', ServicePaymentAPIView.as_view(), name='service_payment'),
]
