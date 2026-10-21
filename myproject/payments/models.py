from django.db import models
from base.models import UserProfile, RentalRequest

TRANSACTION_TYPES = (
    ('PAYMENT', 'Payment'),
    ('REFUND', 'Refund'),
    ('DEPOSIT', 'Deposit'),
    ('WITHDRAW', 'Withdraw'),
)

class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions')
    rental_request = models.ForeignKey(RentalRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    txn_id = models.CharField(max_length=255, blank=True) # to store Razorpay id
    txn_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.txn_type} — {self.amount} — {self.user}"
