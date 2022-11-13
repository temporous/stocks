from typing import Any, Generator, Iterator

from django.db.models import Model
from graphene import ObjectType as BaseObjectType
from graphene import relay
from graphene.types.objecttype import ObjectTypeMeta
from graphene_django import DjangoObjectType as BaseDjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from inventory.models import Portfolio, Stock, Trade

inventory_models = [Portfolio, Stock, Trade]
