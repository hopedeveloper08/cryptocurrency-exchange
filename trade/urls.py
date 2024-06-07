from django.urls import path
from trade.views import Trade

urlpatterns = [
    path('', Trade.as_view(), name='trade'),
]
