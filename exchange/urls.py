from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
    path('account/', include('account.urls')),
    path('market/', include('market.urls')),
    path('asset/', include('asset.urls')),
    path('ticket/', include('ticket.urls')),
    path('trade/', include('trade.urls')),
]
