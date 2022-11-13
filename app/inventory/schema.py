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


# wrap in a function to get a metaclass factory with optional args
class DjangoObjectsMeta(ObjectTypeMeta):
    """
    Metaclass for DjangoObjects
    """

    def __new__(
        cls,
        name: str,
        bases: tuple[object],
        namespace: dict[str, Any],
        **options: dict[Any, Any],
    ):
        # inject prior to creating class
        a_class = super().__new__(
            cls,
            name,
            bases,
            namespace,
            **options,
        )
        return a_class


class DjangoObjectType(BaseDjangoObjectType, metaclass=DjangoObjectsMeta):
    """
    New DjangoObjectType with a different metaclass - for adding injection capabilities
    to existing nodes or creating new concrete nodes.

    ObjectType subverts __init_subclass__ and DjangoObjectType enforces
    some really stringent checks
    it works off of class Meta unless abstract = True is set and the sole
    property of the meta
    """

    class Meta:
        abstract = True


class OtherObjectsMeta(ObjectTypeMeta):
    def __new__(cls, name, bases, namespace, **options):
        # inject prior to creating class
        a_class = super().__new__(
            cls,
            name,
            bases,
            namespace,
            **options,
        )
        return a_class


class ObjectType(BaseObjectType, metaclass=OtherObjectsMeta):
    """
    New ObjectType similar to our added DjangoObjetType
    """

    pass
