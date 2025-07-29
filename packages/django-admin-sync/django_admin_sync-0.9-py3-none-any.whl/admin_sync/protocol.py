from __future__ import annotations

import abc
import logging
from typing import TYPE_CHECKING, Any, Collection, Callable

from django.core.serializers.json import Deserializer as JsonDeserializer
from django.core.serializers.json import Serializer as JsonSerializer
from django.db import connections, transaction

from .collector import BaseCollector, ForeignKeysCollector
from .compat import deserialize_wrapper
from .exceptions import ProtocolError

if TYPE_CHECKING:
    from django.core.serializers.base import Deserializer, Serializer
    from django.db.models import Model
    from django.http import HttpRequest

    from .types import Collectable


logger = logging.getLogger(__name__)


class BaseProtocol(abc.ABC):
    collector_class: type[BaseCollector] = ForeignKeysCollector
    serializer_class: "type[Serializer]" = JsonSerializer
    deserializer_class: "type[Deserializer] | Callable" = JsonDeserializer

    def __init__(self, request: HttpRequest | None = None) -> None:
        self.request = request
        self.collected_records: int = 0

    @property
    def serializer(self) -> "Serializer":
        return self.serializer_class()

    @abc.abstractmethod
    def serialize(self, collection: Collectable) -> str: ...

    @abc.abstractmethod
    def deserialize(self, payload: str) -> list[list[Any]]: ...

    @abc.abstractmethod
    def collect(self, data: "Collectable") -> Collection[Model]: ...


class LoadDumpProtocol(BaseProtocol):
    using = "default"

    def _priv_collect(self, data: "Collectable") -> Collection[Model]:
        data = self.collect(data)
        self.collected_records = len(data)
        return data

    def collect(self, data: "Collectable") -> Collection[Model]:
        c = self.collector_class(collect_related=True)
        c.collect(data)
        return c.data

    def serialize(self, data: Collectable) -> str:
        data = self._priv_collect(data)
        return self.serializer.serialize(data, use_natural_foreign_keys=True, use_natural_primary_keys=True)

    def deserialize(self, payload: str) -> list[list[Any]]:
        processed = []
        try:
            connection = connections[self.using]
            with connection.constraint_checks_disabled(), transaction.atomic(self.using):
                # check this when django<5 support will be removed
                objects = deserialize_wrapper(self.deserializer_class)(
                    stream_or_string=payload, ignorenonexistent=True, handle_forward_references=True
                )
                for obj in objects:
                    obj.save(using=self.using)
                    processed.append([obj.object._meta.object_name, str(obj.object.pk)])
        except AttributeError as e:
            logger.exception(e)
            raise ProtocolError(e) from None
        return processed
