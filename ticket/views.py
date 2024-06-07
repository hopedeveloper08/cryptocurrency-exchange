from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Ticket


class TicketView(LoginRequiredMixin, View):
    login_url = '/account/login/'
    redirect_field_name = 'login'

    def get(self, request):
        tickets = Ticket.objects.filter(trader=request.user)
        return render(request, 'ticket.html', {'tickets': tickets})

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Ticket.objects.create(trader=request.user, title=title, description=description)
            return redirect('ticket')
        else:
            tickets = Ticket.objects.filter(trader=request.user)
            return render(request, 'ticket.html', {'tickets': tickets, 'error': 'لطفاً همه‌ی فیلدها را پر کنید.'})
