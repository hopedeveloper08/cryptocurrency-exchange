from django.shortcuts import render
from django.views import View
from market.models import Currency


class Market(View):
    def get(self, request):
        currencies = Currency.overview()

        context = {
            'currencies': currencies,
        }
        return render(request, 'market.html', context)


class CurrencyInfo(View):
    def get(self, request, symbol):
        currency = Currency.objects.get(symbol=symbol)
        currency_data = currency.get_info()

        context = {
            'currency_data': currency_data
        }
        return render(request, 'currency info.html', context)


class Signal(View):
    def get(self, request, symbol):
        currency = Currency.objects.get(symbol=symbol)
        signals = currency.get_signal()

        context = {
            'signals': signals,
            'symbol': symbol,
        }
        return render(request, 'signal.html', context)


class Chart(View):
    def get(self, request, symbol):
        currency = Currency.objects.get(symbol=symbol)
        currency.get_chart()

        return render(request, 'chart.html')
