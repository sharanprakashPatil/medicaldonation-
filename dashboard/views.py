from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from seekers.models import DonationRequest

def home(request):
    # Show some featured/latest requests on home
    featured_requests = DonationRequest.objects.filter(is_verified=True, is_approved=True, is_completed=False)[:3]
    return render(request, 'home.html', {'featured_requests': featured_requests})

@login_required
def dashboard(request):
    user = request.user
    if user.is_seeker:
        user_requests = DonationRequest.objects.filter(user=user)
        return render(request, 'dashboard/seeker_dashboard.html', {'user_requests': user_requests})
    else:
        # For donors or general users
        return render(request, 'dashboard/donor_dashboard.html')
