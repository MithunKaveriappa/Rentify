from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Transaction
from base.models import RentalRequest
from .forms import TransactionForm
from django.conf import settings

## Razorpay Payment
from django.conf import settings
import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@login_required
def rental_payment(request, pk):
    rental_request = get_object_or_404(RentalRequest, pk=pk, renter__user=request.user, status='APPROVED', payment_confirmed=False)
    amount = float(rental_request.calculate_total())
    deposit = float(rental_request.deposit_taken or rental_request.item.deposit_amount or 0)
    total_amount = amount + deposit
    user_profile = request.user.profile

    if request.method == 'POST':
        # Actual payment logic, expects Razorpay payment_id received from client-side JS
        payment_id = request.POST.get('razorpay_payment_id')
        if payment_id:
            Transaction.objects.create(
                user=user_profile,
                rental_request=rental_request,
                txn_id=payment_id,
                txn_type='PAYMENT',
                amount=total_amount,
                metadata={'via':'Razorpay'}
            )
            rental_request.payment_confirmed = True
            rental_request.status = 'ONGOING'
            rental_request.save()
            messages.success(request, "Payment and rental confirmed.")
            return redirect('my_requests')
        else:
            messages.error(request, "Payment failed. Please try again.")

    else:
        # Prepare Razorpay order and context for the template
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order_data = {
            'amount': int(total_amount * 100), # in paise
            'currency': 'INR',
            'receipt': f'rental_{rental_request.id}',
            'payment_capture': 1,
        }
        order = client.order.create(order_data)
        context = {
            'rental_request': rental_request,
            'amount': total_amount,
            'razorpay_order_id': order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'user_profile': user_profile,
        }
        return render(request, 'rental_payment.html', context)

@login_required
def my_transactions(request):
    txns = request.user.profile.transactions.order_by('-created_at')
    return render(request, 'mytransactions.html', {'transactions': txns})

@user_passes_test(lambda u: u.is_staff)
def all_transactions(request):
    txns = Transaction.objects.select_related('user', 'rental_request').order_by('-created_at')
    return render(request, 'alltransactions.html', {'transactions': txns})

@user_passes_test(lambda u: u.is_staff)
def manage_transaction(request, pk):
    txn = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=txn)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated.")
            return redirect('all_transactions')
    else:
        form = TransactionForm(instance=txn)
    return render(request, 'manage_transaction.html', {'form': form})

