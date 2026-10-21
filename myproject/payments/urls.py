from django.urls import path
from . import views

urlpatterns = [
    # Default (can show my transactions)
    path('', views.my_transactions, name='my_transactions'),

    # Rental payment route with Razorpay for approved request
    path('rental-payment/<int:pk>/', views.rental_payment, name='rental_payment'),

    # Admin views for transactions
    path('all/', views.all_transactions, name='all_transactions'),
    path('manage/<int:pk>/', views.manage_transaction, name='manage_transaction'),
]
