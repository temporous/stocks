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


# filter fields can be added here
filter_field_settings_that_could_come_from_json_or_db: dict[str, dict] = dict(
    PortfolioGrapheneNode=dict(
        name=["exact", "istartswith", "icontains"],
        portfolio_id=["exact"],
    ),
    StockGrapheneNode=dict(
        symbol=["exact"],
        iex_id=["exact"],
        stock_id=["exact"],
    ),
)


def InjectFilter(name: str, namespace: dict[str, Any]):
    if extra_filters := filter_field_settings_that_could_come_from_json_or_db.get(name):
        if meta := namespace.get("Meta"):
            if filters := getattr(meta, "filter_fields"):
                if isinstance(filters, dict):
                    extra_filters = extra_filters | filters
            meta.filter_fields = extra_filters


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
        InjectFilter(name, namespace)
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


def node_name_from_model(a_model: Model, suffix: str = "GrapheneNode"):
    return a_model.__name__ + suffix


def node_factory(models: list[Model]) -> Generator[BaseDjangoObjectType, None, None]:
    for a_model in models:
        yield a_model, DjangoObjectsMeta(
            node_name_from_model(a_model),
            (BaseDjangoObjectType,),
            dict(Meta=MetaFactory(a_model)),
        )


def query_factory(name: str, nodes: Iterator[BaseDjangoObjectType]) -> ObjectType:
    endpoints = {}

    for node in nodes:
        endpoints = endpoints | {
            "all_" + node.__name__: DjangoFilterConnectionField(node),
            node.__name__: relay.Node.Field(node),
        }
    Query = OtherObjectsMeta(name, (ObjectType,), endpoints)
    return Query


nodes = dict(node_factory(inventory_models))

InventoryQuery = query_factory("InventoryQuery", nodes.values())
