from django.db import models
from account.models import Trader


class Ticket(models.Model):
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    status_response = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.trader} {self.title}'
