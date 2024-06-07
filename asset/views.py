from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from market.models import Currency
from asset.models import Asset


class Assets(LoginRequiredMixin, View):
    login_url = '/account/login/'
    redirect_field_name = 'login'

    def get(self, request):
        assets_data = list(map(
            lambda currency: Asset.get_assets_trader(request.user, currency),
            Currency.objects.all()
        ))
        sorted_assets_data = sorted(assets_data, key=lambda asset: asset['value'], reverse=True)

        balance = 0
        for asset in sorted_assets_data:
            balance += asset['value']

        context = {
            'assets_data': sorted_assets_data,
            'balance': balance,
        }
        return render(request, 'asset.html', context)


class Deposit(LoginRequiredMixin, View):
    login_url = '/account/login/'
    redirect_field_name = 'login'

    def get(self, request):
        if not request.user.verification_status:
            return redirect('verify')

        currency_symbol = 'USDT'
        currency = Currency.objects.get(symbol=currency_symbol)
        try:
            asset = Asset.objects.get(trader=request.user, currency=currency)
            current_amount = asset.amount
        except Asset.DoesNotExist:
            current_amount = 0

        context = {
            'currency': currency_symbol,
            'current_amount': current_amount,
            'currency_logo': currency.get_logo_url(),
            'credit_card': request.user.credit_card_number,
        }
        return render(request, 'deposit.html', context)

    def post(self, request):
        if not request.user.verification_status:
            return redirect('verification')

        amount = request.POST.get('amount')
        currency_symbol = request.POST.get('currency')
        currency = Currency.objects.get(symbol=currency_symbol)
        trader = request.user

        try:
            asset = Asset.objects.get(trader=trader, currency=currency)
        except Asset.DoesNotExist:
            asset = Asset(trader=trader, currency=currency)

        asset.deposit(amount)
        messages.success(request, 'واریز با موفقیت انجام شد.')
        return redirect('assets')


class Withdraw(LoginRequiredMixin, View):
    login_url = '/account/login/'
    redirect_field_name = 'login'

    def get(self, request):
        if not request.user.verification_status:
            return redirect('verify')

        currency_symbol = 'USDT'
        currency = Currency.objects.get(symbol=currency_symbol)
        try:
            asset = Asset.objects.get(trader=request.user, currency=currency)
            current_amount = asset.amount
        except Asset.DoesNotExist:
            current_amount = 0

        context = {
            'currency': currency_symbol,
            'current_amount': current_amount,
            'currency_logo': currency.get_logo_url(),
            'credit_card': request.user.credit_card_number,
        }
        return render(request, 'withdraw.html', context)

    def post(self, request):
        if not request.user.verification_status:
            return redirect('verification')

        amount = request.POST.get('amount')
        currency_symbol = request.POST.get('currency')
        currency = Currency.objects.get(symbol=currency_symbol)
        trader = request.user

        try:
            asset = Asset.objects.get(trader=trader, currency=currency)
        except Asset.DoesNotExist:
            asset = Asset(trader=trader, currency=currency)

        result = asset.withdraw(amount)
        if result:
            messages.success(request, 'برداشت با موفقیت انجام شد.')
        else:
            messages.error(request, 'موجودی کافی نیست!')
        return redirect('assets')
