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
    uploaded_types = set(docs.values_list('document_type', flat=True))
    required_docs = [
        ('CERT', 'Medical Certificate', 'Doctor-signed medical certificate confirming diagnosis'),
        ('ID', 'Identity Proof', 'Aadhaar, PAN, Passport or any Govt. ID'),
        ('BANK', 'Bank Passbook', 'Bank passbook or cancelled cheque for fund transfer'),
    ]
    return render(request, 'seekers/upload_documents.html', {
        'form': form,
        'donation_request': donation_request,
        'docs': docs,
        'uploaded_types': uploaded_types,
        'required_docs': required_docs,
    })

@login_required
def submit_for_review(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk, user=request.user)
    uploaded_types = set(donation_request.documents.values_list('document_type', flat=True))
    if 'CERT' in uploaded_types and 'ID' in uploaded_types and 'BANK' in uploaded_types:
        donation_request.is_submitted = True
        donation_request.save()
        messages.success(request, "Your campaign has been submitted for admin review.")
    else:
        messages.error(request, "Please upload all 3 required documents before submitting.")
    return redirect('my_requests')

@login_required
def cancel_campaign(request, pk):
    donation_request = get_object_or_404(DonationRequest, pk=pk, user=request.user)
    if donation_request.is_approved:
        messages.error(request, "Cannot cancel an approved campaign. Contact admin.")
    else:
        donation_request.is_cancelled = True
        donation_request.save()
        messages.success(request, f"Campaign '{donation_request.title}' has been cancelled.")
    return redirect('my_requests')

@login_required
def my_requests(request):
    requests = DonationRequest.objects.filter(user=request.user)
    return render(request, 'seekers/my_requests.html', {'requests': requests})
