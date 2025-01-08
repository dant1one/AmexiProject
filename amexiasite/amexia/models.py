from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Statistic(models.Model):
    currency = models.CharField(max_length=50, unique=True)
    total_buy = models.FloatField(default=0)
    avg_buy = models.FloatField(default=0)
    total_sell = models.FloatField(default=0)
    avg_sell = models.FloatField(default=0)
    profit = models.FloatField(default=0)

    def update_statistics(self, amount, rate, trade):
        if amount <= 0 or rate <= 0:
            raise ValueError("Amount and rate must be positive numbers.")

        if trade == 'buy':
            total_before = self.total_buy
            self.total_buy += amount
            self.avg_buy = (
                (self.avg_buy * total_before) + (amount * rate)
            ) / self.total_buy if self.total_buy > 0 else 0

        elif trade == 'sell':
            total_before = self.total_sell
            self.total_sell += amount
            self.avg_sell = (
                (self.avg_sell * total_before) + (amount * rate)
            ) / self.total_sell if self.total_sell > 0 else 0

        self.profit = (self.total_sell * self.avg_sell) - (self.total_buy * self.avg_buy)

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
        if self.amount <= 0 or self.rate <= 0:
            raise ValueError("Amount and rate must be positive numbers.")

        self.total = round(self.amount * self.rate, 2)

        statistic, created = Statistic.objects.get_or_create(currency=self.currency)

        try:
            statistic.update_statistics(self.amount, self.rate, self.trade)
        except ValueError as e:
            raise ValueError(f"Failed to update statistics: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trade} {self.amount} {self.currency} at {self.rate}"

class Currency(models.Model):
    currency = models.CharField(max_length=50)

    def __str__(self):
        return self.currency
