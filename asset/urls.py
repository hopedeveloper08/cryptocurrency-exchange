from django.urls import path
from asset.views import Assets, Deposit, Withdraw


urlpatterns = [
    path('', Assets.as_view(), name='assets'),
    path('deposit/', Deposit.as_view(), name='deposit'),
    path('withdraw/', Withdraw.as_view(), name='withdraw'),
]
