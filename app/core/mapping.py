# app/core/mapping.py
from typing import Iterable, Type, TypeVar, List
from pydantic import TypeAdapter

T = TypeVar("T")

def to_dto(dto_cls: Type[T], obj) -> T:
    # 1 objeto (ORM o dict)
    return dto_cls.model_validate(obj)

def to_dtos(dto_cls, rows):
    return [dto_cls.model_validate(r, from_attributes=True) for r in rows]
