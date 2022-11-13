import graphene
from inventory.schema import InventoryQuery


class Query(InventoryQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
