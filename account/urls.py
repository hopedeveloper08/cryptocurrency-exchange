from django.urls import path
from account.views import Login, Register, Verify, Account


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('verify/', Verify.as_view(), name='verify'),
    path('', Account.as_view(), name='account'),
]
