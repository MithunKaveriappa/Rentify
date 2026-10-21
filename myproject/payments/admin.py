from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('txn_id', 'user', 'txn_type', 'amount', 'created_at', 'rental_request')
    list_filter = ('txn_type',)
    search_fields = ('txn_id', 'user__user__username')
