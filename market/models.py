from django.db import models
from market.chart import draw_chart
from market.signal import indicators_result
import yfinance as yf
from threading import Thread


class Currency(models.Model):
    name = models.CharField(max_length=32)
    symbol = models.CharField(max_length=5, unique=True, primary_key=True)

    def __str__(self):
        return self.symbol

    @classmethod
    def overview(cls):
        currencies = Currency.objects.all()
        data = list()

        threads = list()
        for currency in currencies:
            thread = Thread(target=lambda: data.append(currency.get_info()))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        sorted_data = sorted(data, key=lambda k: k['marketCap'], reverse=True)
        return sorted_data

    def get_logo_url(self):
        return f'https://raw.githubusercontent.com/Pymmdrza/Cryptocurrency_Logos/mainx/PNG/{self.symbol.lower()}.png'

    def get_price(self):
        return yf.Ticker(f'{self.symbol}-USD').fast_info['lastPrice']

    def get_info(self):
        required_fields = (
            'dayHigh',
            'dayLow',
            'volume',
            'open',
            'previousClose',
            'marketCap',
            'coinMarketCapLink',
            'description',
        )

        try:
            data = yf.Ticker(f'{self.symbol}-USD').info
            price = self.get_price()
        except Exception as e:
            raise e

        filtered_data = dict(filter(
            lambda item: item[0] in required_fields,
            data.items()
        ))

        change_today = (price - filtered_data['previousClose']) * 100 / price
        more_data = {
            'symbol': self.symbol,
            'name': self.name,
            'logo': self.get_logo_url(),
            'price': price,
            'change_today': change_today,
        }

        for key, value in more_data.items():
            filtered_data[key] = value

        return filtered_data

    def get_signal(self):
        try:
            result = indicators_result(self.symbol)
        except Exception as e:
            raise e

        return result

    def get_chart(self):
        try:
            draw_chart(self.symbol)
        except Exception as e:
            raise e
