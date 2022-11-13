from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Stock(models.Model):
    class StockTypes(models.TextChoices):
        NA = "N/A", _("Regular stock")
        CRYPTO = "crypto", _("Crypto currency")

    stock_id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=8)
    name = models.CharField(max_length=28)
    date = models.DateField(default=timezone.now)
    is_enabled = models.BooleanField(null=True)
    stock_type = models.CharField(
        max_length=16, choices=StockTypes.choices, default=StockTypes.NA
    )
    iex_id = models.IntegerField()


class Portfolio(models.Model):
    portfolio_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    initial_account_balance = models.PositiveIntegerField()
    balance = models.PositiveIntegerField(blank=True)

    def save(self, *args, **kwargs):
        if not self.portfolio_id:
            self.balance = self.initial_account_balance
        super().save(*args, **kwargs)


class Trade(models.Model):
    class TradeTypes(models.IntegerChoices):
        BUY = 1, _("Buy")
        SELL = 2, _("Sell")

    trade_id = models.AutoField(primary_key=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
    volume = models.PositiveIntegerField()
    trade_type = models.IntegerField(choices=TradeTypes.choices)


class PortfolioStocks(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    volume = models.PositiveIntegerField()
