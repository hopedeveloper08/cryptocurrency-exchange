from django.urls import path
from ticket.views import TicketView


urlpatterns = [
    path('', TicketView.as_view(), name='ticket'),
]
