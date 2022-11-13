import graphene
from inventory.mutations import InventoryMutation
from inventory.schema import InventoryQuery


class Query(InventoryQuery, graphene.ObjectType):
    pass


class Mutations(InventoryMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
