import razorpay
import io
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from seekers.models import DonationRequest
from .models import PaymentTransaction, CampaignPayout
from donations.models import Donation
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

# Initialize Razorpay Client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
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
            # Fetch payment method from Razorpay
            try:
                payment_info = client.payment.fetch(payment_id)
                method_map = {
                    'card': 'Credit/Debit Card',
                    'netbanking': 'Net Banking',
                    'upi': 'UPI',
                    'wallet': 'Wallet',
                    'emi': 'EMI',
                }
                raw_method = payment_info.get('method', '')
                transaction.payment_method = method_map.get(raw_method, raw_method.upper() if raw_method else 'Unknown')
            except Exception:
                transaction.payment_method = 'Razorpay'
            transaction.save()
            
            # Update Donation Request
            donation_request = transaction.request
            donation_request.amount_raised += transaction.amount
            if donation_request.amount_raised >= donation_request.goal_amount:
                donation_request.is_completed = True
            donation_request.save()
            
            # Record Donation
            donor_name = "Anonymous"
            if request.user.is_authenticated:
                donor_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            donation = Donation.objects.create(
                donor=request.user if request.user.is_authenticated else None,
                request=donation_request,
                amount=transaction.amount,
                payment_id=payment_id,
                order_id=order_id,
                donor_name=donor_name,
                donor_email=request.user.email if request.user.is_authenticated else "anonymous@example.com"
            )
            
            context = {
                'transaction': transaction,
                'donation': donation,
                'donation_request': donation_request,
                'donor_name': donor_name,
            }
            return render(request, 'payments/payment_success.html', context)
            
        except Exception as e:
            if order_id:
                transaction = PaymentTransaction.objects.filter(order_id=order_id).first()
                if transaction:
                    transaction.status = 'FAILED'
                    transaction.save()
            return render(request, 'payments/payment_failed.html')
    
    return redirect('home')

@staff_member_required(login_url='login')
def transfer_funds(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk)

    if not all([donation_request.account_holder_name, donation_request.account_number, donation_request.ifsc_code]):
        messages.error(request, "Seeker has not provided complete bank details.")
        return redirect('admin_dashboard')

    if donation_request.is_granted:
        messages.warning(request, "Funds already transferred for this campaign.")
        return redirect('admin_dashboard')

    amount_paise = int(donation_request.amount_raised * 100)
    if amount_paise <= 0:
        messages.error(request, "No funds to transfer.")
        return redirect('admin_dashboard')

    payout = CampaignPayout.objects.create(
        request=donation_request,
        amount=donation_request.amount_raised,
        payout_status='PROCESSING',
    )

    try:
        contact = client.contact.create({
            "name": donation_request.account_holder_name,
            "email": donation_request.user.email,
            "type": "vendor",
        })

        fund_account = client.fund_account.create({
            "contact_id": contact['id'],
            "account_type": "bank_account",
            "bank_account": {
                "name": donation_request.account_holder_name,
                "ifsc": donation_request.ifsc_code,
                "account_number": donation_request.account_number,
            },
        })

        rp_payout = client.payout.create({
            "fund_account_id": fund_account['id'],
            "amount": amount_paise,
            "currency": "INR",
            "mode": "IMPS",
            "purpose": "payout",
            "queue_if_low_balance": True,
            "reference_id": f"camp_{donation_request.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}",
            "narration": f"Funds transfer for {donation_request.title}",
        })

        payout.fund_account_id = fund_account['id']
        payout.payout_id = rp_payout['id']
        status = rp_payout.get('status', '').upper()
        payout.payout_status = 'SUCCESS' if status == 'PROCESSED' else status
        payout.utr = rp_payout.get('utr', '')
        payout.processed_at = timezone.now()
        payout.save()

        donation_request.is_granted = True
        donation_request.save()

        messages.success(request, f"₹{donation_request.amount_raised} transferred successfully to {donation_request.account_holder_name}.")
        return redirect('payout_receipt', pk=payout.pk)

    except Exception as e:
        payout.payout_status = 'FAILED'
        payout.save()
        messages.error(request, f"Transfer failed: {str(e)}")
        return redirect('admin_dashboard')

def render_pdf(template_path, context):
    html = render_to_string(template_path, context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode('utf-8')), result)
    if pdf.err:
        return None
    return result.getvalue()

@staff_member_required(login_url='login')
def payout_receipt(request, pk):
    payout = get_object_or_404(CampaignPayout, pk=pk)
    if 'pdf' in request.GET:
        pdf = render_pdf('payments/payout_receipt_content.html', {'payout': payout})
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f"payout_receipt_{payout.id}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        messages.error(request, "Failed to generate PDF.")
    return render(request, 'payments/payout_receipt.html', {'payout': payout})

@login_required
def seeker_payout_receipt(request, pk):
    payout = get_object_or_404(CampaignPayout, pk=pk, request__user=request.user)
    pdf = render_pdf('payments/payout_receipt_content.html', {'payout': payout})
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"payout_receipt_{payout.id}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    messages.error(request, "Failed to generate PDF.")
    return redirect('my_requests')
