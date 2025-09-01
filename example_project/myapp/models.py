from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from post_fetch_hook.models import PostFetchModel

if TYPE_CHECKING:
    from post_fetch_hook.typing import Any


class Parent(PostFetchModel):
    obj = models.ForeignKey(to="Object", on_delete=models.SET_NULL, null=True, related_name="parents")
    title = models.CharField(null=True, max_length=20)

    @classmethod
    def post_fetch_hook(cls, model: Parent) -> Parent:
        model.title = None
        return model


class Object(PostFetchModel):
    thing = models.ForeignKey(to="Thing", on_delete=models.CASCADE, related_name="objs")
    identifier = models.IntegerField(null=True)

    @classmethod
    def post_fetch_hook(cls, model: Object) -> Object:
        model.identifier = None
        return model


class Thing(PostFetchModel):
    name = models.CharField(null=True, max_length=20)
    age = models.IntegerField(null=True)
    email = models.EmailField(null=True)

    @classmethod
    def post_fetch_hook(cls, model: Thing) -> Thing:
        model.name = None
        model.age = None
        model.email = None
        return model

    @classmethod
    def post_fetch_values_hook(cls, values: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
        return dict(zip(values, fields))  # noqa: B905

    @classmethod
    def post_fetch_values_list_hook(cls, values: tuple[Any, ...], fields: tuple[str, ...]) -> tuple[Any, ...]:
        return fields

    @classmethod
    def post_fetch_values_list_flat_hook(cls, value: Any, field: str) -> Any:
        return field
