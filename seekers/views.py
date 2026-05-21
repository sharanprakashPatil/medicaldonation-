from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DonationRequest, MedicalDocument
from .forms import DonationRequestForm, MedicalDocumentForm
from django.contrib import messages

@login_required
def create_request(request):
    if not request.user.is_seeker:
        messages.error(request, "Only seekers can create requests.")
        return redirect('home')
    
    if request.method == 'POST':
        form = DonationRequestForm(request.POST)
        if form.is_valid():
            donation_request = form.save(commit=False)
            donation_request.user = request.user
            donation_request.save()
            messages.success(request, "Request created! Now upload required medical documents.")
            return redirect('upload_documents', pk=donation_request.pk)
    else:
        form = DonationRequestForm()
    return render(request, 'seekers/create_request.html', {'form': form})

@login_required
def upload_documents(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = MedicalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.request = donation_request
            doc.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect('upload_documents', pk=pk)
    else:
        form = MedicalDocumentForm()
    
    docs = donation_request.documents.all()
    return render(request, 'seekers/upload_documents.html', {'form': form, 'donation_request': donation_request, 'docs': docs})

@login_required
def my_requests(request):
    requests = DonationRequest.objects.filter(user=request.user)
    return render(request, 'seekers/my_requests.html', {'requests': requests})
