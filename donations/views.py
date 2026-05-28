from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from seekers.models import DonationRequest
from payments.models import PaymentTransaction
from .models import Donation

def donation_list(request):
    # Only show verified and approved requests that are not rejected
    query = request.GET.get('q')
    if query:
        requests = DonationRequest.objects.filter(is_verified=True, is_approved=True, is_completed=False, is_rejected=False, title__icontains=query)
    else:
        requests = DonationRequest.objects.filter(is_verified=True, is_approved=True, is_completed=False, is_rejected=False)
    total_campaigns = requests.count()
    total_goal = sum(r.goal_amount for r in requests)
    total_raised = sum(r.amount_raised for r in requests)
    return render(request, 'donations/donation_list.html', {
        'requests': requests,
        'total_campaigns': total_campaigns,
        'total_goal': total_goal,
        'total_raised': total_raised,
    })

def donation_detail(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk, is_verified=True, is_approved=True, is_rejected=False)
    return render(request, 'donations/donation_detail.html', {'donation_request': donation_request})

@login_required
def my_donations(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-timestamp')
    total_donated = sum(d.amount for d in donations)
    context = {
        'donations': donations,
        'total_donated': total_donated,
        'count': donations.count(),
    }
    return render(request, 'donations/my_donations.html', context)

@login_required
def donation_receipt(request, pk):
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    transaction = PaymentTransaction.objects.filter(payment_id=donation.payment_id).first()
    context = {
        'donation': donation,
        'transaction': transaction,
        'donation_request': donation.request,
        'donor_name': donation.donor_name,
    }
    return render(request, 'donations/receipt.html', context)
