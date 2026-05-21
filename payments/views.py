import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from seekers.models import DonationRequest
from .models import PaymentTransaction
from donations.models import Donation
from django.contrib import messages

# Initialize Razorpay Client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def initiate_payment(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    amount = request.POST.get('amount')
    
    if not amount:
        messages.error(request, "Please enter an amount.")
        return redirect('donation_detail', pk=pk)
    
    # Amount in paise
    razorpay_amount = int(float(amount) * 100)
    
    try:
        order = client.order.create({
            'amount': razorpay_amount,
            'currency': 'INR',
            'payment_capture': '1'
        })
    except Exception as e:
        messages.error(request, f"Payment gateway error: {str(e)}")
        return redirect('donation_detail', pk=pk)
    
    PaymentTransaction.objects.create(
        request=donation_request,
        amount=amount,
        order_id=order['id'],
        status='PENDING'
    )
    
    context = {
        'order_id': order['id'],
        'amount': amount,
        'razorpay_amount': razorpay_amount,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'donation_request': donation_request,
        'user': request.user
    }
    return render(request, 'payments/payment_page.html', context)

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        try:
            # Verify signature
            client.utility.verify_payment_signature(params_dict)
            
            transaction = PaymentTransaction.objects.get(order_id=order_id)
            transaction.payment_id = payment_id
            transaction.signature = signature
            transaction.status = 'SUCCESS'
            transaction.save()
            
            # Update Donation Request
            donation_request = transaction.request
            donation_request.amount_raised += transaction.amount
            if donation_request.amount_raised >= donation_request.goal_amount:
                donation_request.is_completed = True
            donation_request.save()
            
            # Record Donation
            Donation.objects.create(
                donor=request.user if request.user.is_authenticated else None,
                request=donation_request,
                amount=transaction.amount,
                payment_id=payment_id,
                order_id=order_id,
                donor_email=request.user.email if request.user.is_authenticated else "anonymous@example.com"
            )
            
            return render(request, 'payments/payment_success.html', {'transaction': transaction})
            
        except Exception as e:
            if order_id:
                transaction = PaymentTransaction.objects.filter(order_id=order_id).first()
                if transaction:
                    transaction.status = 'FAILED'
                    transaction.save()
            return render(request, 'payments/payment_failed.html')
    
    return redirect('home')
