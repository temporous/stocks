from typing import Any, Generator, Iterator

from django.db.models import Model
from graphene import ObjectType as BaseObjectType
from graphene import relay
from graphene.types.objecttype import ObjectTypeMeta
from graphene_django import DjangoObjectType as BaseDjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from inventory.models import Portfolio, Stock, Trade

inventory_models = [Portfolio, Stock, Trade]


def MetaFactory(a_model: Model, exclude: list[str] = []):
    """
    Class factory to create Meta models required for django graphene
    """
    fields = tuple(
        f.name
        for f in a_model._meta.get_fields()
        if f.concrete and not f.name in exclude
    )

    class Meta:
        model = a_model
        fields = "__all__"
        filter_fields = fields
        interfaces = (relay.Node,)

    return Meta
