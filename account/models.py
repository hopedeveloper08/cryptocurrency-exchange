from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login


class Trader(AbstractUser):
    verification_status = models.BooleanField(default=False)
    credit_card_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

    def login_user(self, request):
        try:
            login(request, self)
            return True
        except:
            return False

    def register_user(self, username, password):
        try:
            self.username = username
            self.set_password(password)
            self.save()
            return True
        except:
            return False

    def verify_user(self, creditcard_number):
        self.credit_card_number = creditcard_number
        self.verification_status = True
        self.save()
        return True
