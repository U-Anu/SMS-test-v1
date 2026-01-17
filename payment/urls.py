from django.urls import path
from payment import views
urlpatterns=[
    path('fees_payment/<pk>',views.fees_payment,name='fees_payment'),
    path('payment-status', views.payment_status, name='payment-status')
]