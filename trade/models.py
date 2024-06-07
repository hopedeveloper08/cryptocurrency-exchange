from django.db import models
from account.models import Trader
from market.models import Currency
from asset.models import Asset


class Order(models.Model):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    is_buy = models.BooleanField()
    amount = models.FloatField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.trader.username} {"خرید" if self.is_buy else "فروش"} {self.currency} {self.amount}'

    @classmethod
    def buy(cls, trader, currency, amount):
        current_price = currency.get_price()
        has_balance = cls.check_balance(trader, 'USDT', amount * current_price)
        if not has_balance:
            return False

        order = cls.objects.create(
            trader=trader,
            currency=currency,
            is_buy=True,
            amount=amount,
        )

        return order.transaction_buy(current_price)

    @classmethod
    def sell(cls, trader, currency, amount):
        has_balance = cls.check_balance(trader, currency.symbol, amount)
        if not has_balance:
            return False

        current_price = currency.get_price()
        order = cls.objects.create(
            trader=trader,
            currency=currency,
            is_buy=False,
            amount=amount,
        )

        return order.transaction_sell(current_price)

    @staticmethod
    def check_balance(trader, symbol, amount):
        try:
            asset = Asset.objects.get(trader=trader, currency__symbol=symbol)
        except Asset.DoesNotExist:
            return False

        if asset.amount < amount:
            return False

        return True

    def transaction_buy(self, current_price):
        usdt = Asset.objects.get(trader=self.trader, currency__symbol='USDT')
        result = usdt.withdraw(self.amount * current_price)

        if not result:
            return False

        try:
            asset = Asset.objects.get(trader=self.trader, currency=self.currency)
            return asset.deposit(self.amount)
        except Asset.DoesNotExist:
            Asset.objects.create(trader=self.trader, currency=self.currency, amount=self.amount)
            return True

    def transaction_sell(self, current_price):
        asset = Asset.objects.get(trader=self.trader, currency=self.currency)
        result = asset.withdraw(self.amount)

        if not result:
            return False

        try:
            usdt = Asset.objects.get(trader=self.trader, currency__symbol='USDT')
            return usdt.deposit(self.amount * current_price)
        except:
            Asset.objects.create(trader=self.trader, currency='USDT', amount=self.amount)
            return True
