from django.db import models
from account.models import Trader
from market.models import Currency


class Asset(models.Model):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)

    def __str__(self):
        return f'{self.amount} {self.currency} {self.trader}'

    def get_value(self):
        return self.amount * self.currency.get_price()

    def deposit(self, amount):
        amount = float(amount)
        if amount < 0:
            return False

        self.amount += amount
        self.save()
        return True

    def withdraw(self, amount):
        amount = float(amount)
        if amount > self.amount or amount < 0:
            return False

        self.amount -= amount
        self.save()
        return True

    @staticmethod
    def get_assets_trader(trader, currency):
        try:
            asset = Asset.objects.get(trader=trader, currency=currency)
            amount = asset.amount
            value = asset.get_value()
        except Asset.DoesNotExist:
            amount = 0
            value = 0

        return {
            'name': currency.name,
            'symbol': currency.symbol,
            'logo': currency.get_logo_url(),
            'amount': amount,
            'value': value,
        }
