from django.shortcuts import render, get_object_or_404
from seekers.models import DonationRequest

def donation_list(request):
    # Only show verified and approved requests
    query = request.GET.get('q')
    if query:
        requests = DonationRequest.objects.filter(is_verified=True, is_approved=True, is_completed=False, title__icontains=query)
    else:
        requests = DonationRequest.objects.filter(is_verified=True, is_approved=True, is_completed=False)
    return render(request, 'donations/donation_list.html', {'requests': requests})

def donation_detail(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk, is_verified=True, is_approved=True)
    return render(request, 'donations/donation_detail.html', {'donation_request': donation_request})
