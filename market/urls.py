from django.urls import path
from market.views import Market, CurrencyInfo, Signal, Chart

urlpatterns = [
    path('', Market.as_view(), name='market'),
    path('<str:symbol>/', CurrencyInfo.as_view(), name='currency_info'),
    path('chart/<str:symbol>/', Chart.as_view(), name='chart'),
    path('signal/<str:symbol>', Signal.as_view(), name='signal'),
]
