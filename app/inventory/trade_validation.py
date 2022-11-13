from inventory.models import Portfolio, PortfolioStocks, Stock, Trade


class TradeError(Exception):
    pass


def PerformTrade(trade: Trade):
    """
    Creating a trade additionally needs to verify
    validity and update ProfileStocks
    """
    stock = trade.stock
    portfolio = trade.portfolio
    portfolio_stock, _created = PortfolioStocks.objects.get_or_create(
        portfolio_id=portfolio.portfolio_id,
        stock_id=stock.stock_id,
        defaults=dict(volume=0),
    )
    if trade.trade_type == Trade.TradeTypes.BUY:
        return buy(trade, portfolio, portfolio_stock)
    elif trade.trade_type == Trade.TradeTypes.SELL:
        return sell(trade, portfolio, portfolio_stock, stock)
    else:
        raise TradeError("Erroneous trade type")


def buy(trade: Trade, portfolio: Portfolio, portfolio_stock: PortfolioStocks):
    if not portfolio_has_balance(trade, portfolio):
        raise TradeError(
            f"Cannot perform trade as portfolio balance ({portfolio.balance}) less than cost ({trade_balance(trade)})"
        )
    portfolio_stock.volume += trade.volume
    portfolio_stock.save()

    portfolio.balance -= trade_balance(trade)
    portfolio.save()


def sell(
    trade: Trade, portfolio: Portfolio, portfolio_stock: PortfolioStocks, stock: Stock
):
    if not portfolio_has_volume(trade, portfolio_stock):
        raise TradeError(
            f"Connot perform trade as portfolio only has {portfolio_stock.volume} of {stock.symbol} when {trade.volume} was requested"
        )

    portfolio_stock.volume -= trade.volume
    portfolio_stock.save()

    portfolio.balance += trade_balance(trade)
    portfolio.save()


def portfolio_has_volume(trade: Trade, portfolio_stock: PortfolioStocks):
    return trade.volume <= portfolio_stock.volume


def portfolio_has_balance(trade: Trade, portfolio: Portfolio):
    return portfolio.balance >= trade_balance(trade)


def trade_balance(trade):
    return trade.volume * trade.price
