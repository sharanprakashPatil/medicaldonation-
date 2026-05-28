from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import SupportTicket

@login_required
def create_ticket(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        message = request.POST.get('message')
        if category and message:
            ticket = SupportTicket.objects.create(
                user=request.user,
                category=category,
                message=message
            )
            messages.success(request, f"Ticket {ticket.ticket_id} created successfully!")
            return redirect('my_tickets')
        else:
            messages.error(request, "Please fill in all fields.")
    return render(request, 'support/create_ticket.html')

@login_required
def my_tickets(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support/my_tickets.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id, user=request.user)
    return render(request, 'support/ticket_detail.html', {'ticket': ticket})

@staff_member_required(login_url='login')
def admin_ticket_list(request):
    tickets = SupportTicket.objects.all().order_by('-created_at')
    return render(request, 'support/admin_ticket_list.html', {'tickets': tickets})

@staff_member_required(login_url='login')
def admin_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
    if request.method == 'POST':
        reply = request.POST.get('admin_reply')
        status = request.POST.get('status')
        if reply:
            ticket.admin_reply = reply
        if status:
            ticket.status = status
        ticket.save()
        messages.success(request, f"Ticket {ticket.ticket_id} updated.")
        return redirect('admin_ticket_list')
    return render(request, 'support/admin_ticket_detail.html', {'ticket': ticket})
