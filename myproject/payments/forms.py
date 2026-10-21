from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['txn_type', 'amount', 'txn_id', 'metadata', 'rental_request']
        widgets = {
            'txn_type': forms.Select(attrs={'class':'form-control'}),
            'amount': forms.NumberInput(attrs={'class':'form-control', 'min':0}),
            'txn_id': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Razorpay ID'}),
            'metadata': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'placeholder':'Transaction metadata (if any)'}),
            'rental_request': forms.Select(attrs={'class':'form-control'}),
        }
