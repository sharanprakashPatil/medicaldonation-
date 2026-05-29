from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from seekers.models import DonationRequest
from .models import MedicalBlog

def home(request):
    blogs = MedicalBlog.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {'blogs': blogs})

def blog_list(request):
    blogs = MedicalBlog.objects.filter(is_active=True)
    return render(request, 'dashboard/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(MedicalBlog, pk=pk, is_active=True)
    recent = MedicalBlog.objects.filter(is_active=True).exclude(pk=pk)[:3]
    return render(request, 'dashboard/blog_detail.html', {'blog': blog, 'recent': recent})

@login_required
def dashboard(request):
    user = request.user
    if user.is_staff:
        return redirect('admin_dashboard')
    if user.is_seeker:
        user_requests = DonationRequest.objects.filter(user=user)
        return render(request, 'dashboard/seeker_dashboard.html', {'user_requests': user_requests})
    elif user.is_donor:
        return render(request, 'dashboard/donor_dashboard.html')
    else:
        return render(request, 'dashboard/donor_dashboard.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, f"Thank you {name}! We have received your message and will get back to you soon.")
        return redirect('contact')
    return render(request, 'contact.html')
