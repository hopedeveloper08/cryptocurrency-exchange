from django.contrib import admin
from ticket.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('trader', 'title', 'status_response')
    list_display_links = ('title',)
    list_editable = ('status_response',)
