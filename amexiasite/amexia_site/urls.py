from django.contrib import admin
from django.urls import path
from amexia.views import (UserAPIView, CurrencyAPIView, AddCurrency,
                          Login, AddExchange,ExchangeAPIView, StatisticAPIView, SignUpView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', SignUpView.as_view(), name='register'),
    path('api/login/', Login.as_view(), name='login'),
    path('api/addcurrency/', AddCurrency.as_view(), name='currency'),
    path('api/userlist/', UserAPIView.as_view(), name='userlist'),
    path('api/currencylist/', CurrencyAPIView.as_view(), name='currencylist'),
    path('api/exchangelist/', ExchangeAPIView.as_view(), name='exchangelist'),
    path('api/statisticlist/', StatisticAPIView.as_view(), name='statisticlist'),
    path('api/addexchange/', AddExchange.as_view(), name='exchange'),
]
