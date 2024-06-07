from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from account.models import Trader


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        trader = Trader()
        registration_successful = trader.register_user(username, password)

        if registration_successful:
            messages.success(request, 'ثبت نام موفقیت‌آمیز بود.')
        else:
            messages.error(request, 'نام کاربری قبلا انتخاب شده است!')

        return redirect('account')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        trader = authenticate(request, username=username, password=password)
        login_successful = False

        if trader:
            login_successful = trader.login_user(request)

        if login_successful:
            messages.success(request, 'ورود موفقیت‌آمیز بود.')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')

        return redirect('account')


class Verify(LoginRequiredMixin, View):
    login_url = '/account/login/'
    redirect_field_name = 'login'

    def get(self, request):
        return render(request, 'verify.html')

    def post(self, request):
        credit_card = request.POST['credit_card']

        verification_successful = request.user.verify_user(credit_card)
        if verification_successful:
            messages.success(request, 'احراز هویت موفقیت‌آمیز بود.')
        else:
            messages.error(request, 'احراز هویت با مشکل مواجه شد.')
        return redirect('account')


class Account(View):
    def get(self, request):
        return render(request, 'account.html')
