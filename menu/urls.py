from django.urls import path
from menu.views import Menu, AboutUs

urlpatterns = [
    path('', Menu.as_view(), name='menu'),
    path('aboutus/', AboutUs.as_view(), name='aboutus'),
]
