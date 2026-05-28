from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from seekers.models import DonationRequest
from donations.models import Donation
from django.contrib import messages

@staff_member_required(login_url='login')
def admin_dashboard(request):
    unverified_requests = DonationRequest.objects.filter(is_submitted=True, is_verified=False, is_rejected=False)
    unapproved_requests = DonationRequest.objects.filter(is_verified=True, is_approved=False, is_rejected=False)
    approved_requests = DonationRequest.objects.filter(is_approved=True)
    rejected_requests = DonationRequest.objects.filter(is_rejected=True)
    
    context = {
        'unverified': unverified_requests,
        'unapproved': unapproved_requests,
        'approved': approved_requests,
        'rejected': rejected_requests,
    }
    return render(request, 'adminpanel/dashboard.html', context)

@staff_member_required(login_url='login')
def verify_request(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    donation_request.is_verified = True
    donation_request.save()
    messages.success(request, f"Request {pk} has been verified.")
    return redirect('admin_dashboard')

@staff_member_required(login_url='login')
def approve_request(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    donation_request.is_approved = True
    donation_request.save()
    messages.success(request, f"Request {pk} has been approved and is now public.")
    return redirect('admin_dashboard')

@staff_member_required(login_url='login')
def grant_money(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    donation_request.is_granted = True
    donation_request.save()
    messages.success(request, f"Money for Request {pk} has been marked as granted to the seeker.")
    return redirect('admin_dashboard')

@staff_member_required(login_url='login')
def reject_request(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', '')
        donation_request.is_rejected = True
        donation_request.rejection_reason = reason
        donation_request.save()
        messages.success(request, f"Request {pk} has been rejected.")
        return redirect('admin_dashboard')
    return render(request, 'adminpanel/reject_request.html', {'req': donation_request})

@staff_member_required(login_url='login')
def view_documents(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    documents = donation_request.documents.all()
    return render(request, 'adminpanel/view_documents.html', {
        'donation_request': donation_request,
        'documents': documents
    })

@staff_member_required(login_url='login')
def campaign_detail(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    donations = Donation.objects.filter(request=donation_request).order_by('-timestamp')
    total_donors = donations.count()
    context = {
        'campaign': donation_request,
        'donations': donations,
        'total_donors': total_donors,
    }
    return render(request, 'adminpanel/campaign_detail.html', context)

@staff_member_required(login_url='login')
def all_campaigns(request):
    campaigns = DonationRequest.objects.all().order_by('-created_at')
    for c in campaigns:
        c.donation_count = c.public_donations.count()
    total_collected = sum(c.amount_raised for c in campaigns)
    context = {
        'campaigns': campaigns,
        'total_collected': total_collected,
    }
    return render(request, 'adminpanel/all_campaigns.html', context)

@staff_member_required(login_url='login')
def all_transactions(request):
    donations = Donation.objects.select_related('request').order_by('-timestamp')
    total_amount = sum(d.amount for d in donations)
    context = {
        'donations': donations,
        'total_amount': total_amount,
        'total_count': donations.count(),
    }
    return render(request, 'adminpanel/all_transactions.html', context)
