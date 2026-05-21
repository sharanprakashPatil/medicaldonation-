from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from seekers.models import DonationRequest
from django.contrib import messages

@staff_member_required(login_url='login')
def admin_dashboard(request):
    unverified_requests = DonationRequest.objects.filter(is_verified=False)
    unapproved_requests = DonationRequest.objects.filter(is_verified=True, is_approved=False)
    approved_requests = DonationRequest.objects.filter(is_approved=True)
    
    context = {
        'unverified': unverified_requests,
        'unapproved': unapproved_requests,
        'approved': approved_requests
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
def view_documents(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk)
    documents = donation_request.documents.all()
    return render(request, 'adminpanel/view_documents.html', {
        'donation_request': donation_request,
        'documents': documents
    })
