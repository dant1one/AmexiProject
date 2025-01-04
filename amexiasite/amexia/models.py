from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Statistic(models.Model):
    currency = models.CharField(max_length=50, unique=True)
    total_buy = models.IntegerField(default=0)
    avg_buy = models.FloatField(default=0)
    total_sell = models.IntegerField(default=0)
    avg_sell = models.FloatField(default=0)
    profit = models.FloatField(default=0)

    def update_statistics(self, amount, rate, trade):
        if trade == 'buy':
            self.total_buy += amount
            if self.total_buy > 0:
                self.avg_buy = (self.avg_buy * (self.total_buy - amount) + amount * rate) / self.total_buy
        elif trade == 'sell':
            self.total_sell += amount
            if self.total_sell > 0:
                self.avg_sell = (self.avg_sell * (self.total_sell - amount) + amount * rate) / self.total_sell

        self.profit = self.total_sell * self.avg_sell - self.total_buy * self.avg_buy

        self.save()

    def __str__(self):
        return self.currency

class Exchange(models.Model):
    time = models.DateTimeField(default=timezone.now)
    trade = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    amount = models.FloatField()
    rate = models.FloatField()
    total = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.total = self.amount * self.rate

        statistic, created = Statistic.objects.get_or_create(currency=self.currency)

        statistic.update_statistics(self.amount, self.rate, self.trade)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trade} {self.amount} {self.currency} at {self.rate}"

class Currency(models.Model):
    currency = models.CharField(max_length=50)

    def __str__(self):
        return self.currency
