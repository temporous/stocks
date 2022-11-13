from django.contrib import admin

from inventory.models import Portfolio, PortfolioStocks, Stock, Trade

admin.site.register(Portfolio)
admin.site.register(PortfolioStocks)
admin.site.register(Stock)
admin.site.register(Trade)
