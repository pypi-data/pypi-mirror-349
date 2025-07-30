from typing import Type, TypedDict, Protocol, Any
from django.db.models.manager import Manager

class DjangoModelProtocol(Protocol):
    objects: Manager
    _meta: Any

class ObjectTypeDefinition(TypedDict):
    model: Type[DjangoModelProtocol]
    endpoint: str
