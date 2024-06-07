from django.shortcuts import render, redirect
from trade.models import Order
from django.views import View
from market.models import Currency
from django.contrib import messages
from django.urls import reverse
from asset.models import Asset
from django.contrib.auth.mixins import LoginRequiredMixin


class Trade(LoginRequiredMixin, View):
    login_url = '/account/login/'
    redirect_field_name = 'login'

    def get(self, request):
        if not request.user.verification_status:
            return redirect('verify')

        currencies = Currency.objects.exclude(symbol='USDT')
        data = list()
        for currency in currencies:
            try:
                amount = Asset.objects.get(currency=currency, trader=request.user).amount
            except Asset.DoesNotExist:
                amount = 0

            data.append({
                'symbol': currency.symbol,
                'name': currency.name,
                'price': currency.get_price(),
                'logo_url': currency.get_logo_url(),
                'current_amount': amount,
            })

        context = {
            'currencies': data,
        }
        return render(request, 'trade.html', context)

    def post(self, request):
        if not request.user.verification_status:
            return redirect('verify')

        trader = request.user
        symbol = request.POST.get('symbol')
        currency = Currency.objects.get(symbol=symbol)
        is_buy = request.POST.get('order_type') == 'buy'
        amount = float(request.POST.get('amount'))

        if is_buy:
            success = Order.buy(trader, currency, amount)
            action = "خرید"
        else:
            success = Order.sell(trader, currency, amount)
            action = "فروش"

        if success:
            messages.success(request, f'سفارش {action} با موفقیت انجام شد.')
        else:
            messages.error(request, f'سفارش {action} انجام نشد. لطفا موجودی خود را بررسی کنید.')

        return redirect(reverse('trade'))
