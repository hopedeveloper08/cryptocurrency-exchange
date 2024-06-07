from django.shortcuts import render
from django.views import View


class Menu(View):
    def get(self, request):
        return render(request, 'menu.html')


class AboutUs(View):
    def get(self, request):
        return render(request, 'aboutus.html')
