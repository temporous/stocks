import graphene
from django import forms
from django.db import models, transaction
from graphene_django.forms.mutation import DjangoModelFormMutation, Field
from graphene_django.types import ErrorType

from inventory.models import Portfolio, PortfolioStocks, Trade
from inventory.schema import nodes
from inventory.trade_validation import PerformTrade, TradeError


class CreatePortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = (
            "name",
            "description",
            "initial_account_balance",
        )

    def is_valid(self, *args, **kwargs):
        if self.instance.pk:
            self.errors["portfolio_id"] = [
                "Cannot update existing portfolio using Create Portfolio"
            ]
            return False
        return super().is_valid(*args, **kwargs)


class UpdatePortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = (
            "description",
            "name",
        )

    def is_valid(self, *args, **kwargs):
        if not self.instance.pk:
            self.errors["portfolio_id"] = ["Can only update existing portfolio"]
            return False
        return super().is_valid(*args, **kwargs)


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = (
            "portfolio",
            "stock",
            "price",
            "volume",
        )


class CreatePortfolio(DjangoModelFormMutation):
    Portfolio = Field(nodes[Portfolio])

    class Meta:
        form_class = CreatePortfolioForm


class UpdatePortfolio(DjangoModelFormMutation):
    Portfolio = Field(nodes[Portfolio])

    class Meta:
        form_class = UpdatePortfolioForm


class BuyStock(DjangoModelFormMutation):
    Trade = Field(nodes[Trade])

    class Meta:
        form_class = TradeForm

    @classmethod
    def perform_mutate(cls, form, info):
        obj = form.save(commit=False)
        obj.trade_type = Trade.TradeTypes.BUY.value
        errors = []
        try:
            with transaction.atomic():
                obj.save()
                PerformTrade(obj)
        except TradeError as e:
            errors.append(ErrorType(field="trade", messages=[str(e)]))
        if errors:
            return cls(errors=errors)
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)


class SellStock(DjangoModelFormMutation):
    Trade = Field(nodes[Trade])

    class Meta:
        form_class = TradeForm

    @classmethod
    def perform_mutate(cls, form, info):
        obj = form.save(commit=False)
        obj.trade_type = Trade.TradeTypes.SELL.value
        errors = []
        try:
            with transaction.atomic():
                obj.save()
                PerformTrade(obj)
        except TradeError as e:
            errors.append(ErrorType(field="trade", messages=[str(e)]))
        if errors:
            return cls(errors=errors)
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)


class InventoryMutation(graphene.ObjectType):
    create_portfolio = CreatePortfolio.Field()
    buy_stock = BuyStock.Field()
    sell_stock = SellStock.Field()
    update_portfolio = UpdatePortfolio.Field()
