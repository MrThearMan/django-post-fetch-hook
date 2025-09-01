from typing import TYPE_CHECKING

import pytest

from example_project.myapp.models import Object, Parent, Thing

if TYPE_CHECKING:
    from post_fetch_hook.typing import Any


@pytest.mark.django_db
def test_post_fetch_hook() -> None:
    t0 = Thing(name="foo", age=12, email="foo@bar.com")

    assert t0.name == "foo"
    assert t0.age == 12
    assert t0.email == "foo@bar.com"

    t0.save()

    t1: Thing = Thing.objects.first()

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None


@pytest.mark.django_db
def test_post_fetch_values_hook() -> None:
    t0 = Thing(name="foo", age=12, email="foo@bar.com")

    assert t0.name == "foo"
    assert t0.age == 12
    assert t0.email == "foo@bar.com"

    t0.save()

    t1: dict[str, Any] = Thing.objects.values("name", "age").first()

    assert t1["name"] == "name"
    assert t1["age"] == "age"


@pytest.mark.django_db
def test_post_fetch_values_list_hook() -> None:
    t0 = Thing(name="foo", age=12, email="foo@bar.com")

    assert t0.name == "foo"
    assert t0.age == 12
    assert t0.email == "foo@bar.com"

    t0.save()

    t1: tuple[Any, ...] = Thing.objects.values_list("name", "age").first()

    assert t1[0] == "name"
    assert t1[1] == "age"


@pytest.mark.django_db
def test_post_fetch_values_list_flat_hook() -> None:
    t0 = Thing(name="foo", age=12, email="foo@bar.com")

    assert t0.name == "foo"
    assert t0.age == 12
    assert t0.email == "foo@bar.com"

    t0.save()

    t1: Any = Thing.objects.values_list("name", flat=True).first()

    assert t1 == "name"


@pytest.mark.django_db
def test_post_fetch_hook__get() -> None:
    Thing(name="foo", age=12, email="foo@bar.com").save()

    t1: Thing = Thing.objects.get(name="foo")

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None


@pytest.mark.django_db
def test_post_fetch_hook__first() -> None:
    Thing(name="foo", age=12, email="foo@bar.com").save()

    t1: Thing = Thing.objects.first()

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None


@pytest.mark.django_db
def test_post_fetch_hook__last() -> None:
    Thing(name="foo", age=12, email="foo@bar.com").save()

    t1: Thing = Thing.objects.last()

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None


@pytest.mark.django_db
def test_post_fetch_hook__iter() -> None:
    Thing(name="foo", age=12, email="foo@bar.com").save()

    t1: list[Thing] = list(Thing.objects.all())

    assert t1[0].name is None
    assert t1[0].age is None
    assert t1[0].email is None


@pytest.mark.django_db
def test_post_fetch_hook__select_related() -> None:
    thing = Thing(name="foo", age=12, email="foo@bar.com")
    thing.save()

    obj = Object(thing=thing, identifier=0)
    obj.save()

    o1: Object = Object.objects.select_related("thing").first()

    assert o1.identifier is None
    assert o1.thing.name is None
    assert o1.thing.age is None
    assert o1.thing.email is None


@pytest.mark.django_db
def test_post_fetch_hook__select_related__all() -> None:
    thing = Thing(name="foo", age=12, email="foo@bar.com")
    thing.save()

    obj = Object(thing=thing, identifier=0)
    obj.save()

    parent = Parent(obj=obj, title="bar")
    parent.save()

    p1: Parent = Parent.objects.select_related().first()
    print("foo")

    assert p1.title is None
    assert p1.obj.identifier is None
    # select related with no arguments only selects the first level, so new query is made here
    assert p1.obj.thing.name is None
    assert p1.obj.thing.age is None
    assert p1.obj.thing.email is None


@pytest.mark.django_db
def test_post_fetch_hook__select_related__multiple() -> None:
    thing = Thing(name="foo", age=12, email="foo@bar.com")
    thing.save()

    obj = Object(thing=thing, identifier=0)
    obj.save()

    parent = Parent(obj=obj, title="bar")
    parent.save()

    p1: Parent = Parent.objects.select_related("obj__thing").first()

    assert p1.title is None
    assert p1.obj.identifier is None
    assert p1.obj.thing.name is None
    assert p1.obj.thing.age is None
    assert p1.obj.thing.email is None


@pytest.mark.django_db
def test_post_fetch_hook__select_related__null_relation() -> None:
    parent = Parent(obj=None, title="bar")
    parent.save()

    p1: Parent = Parent.objects.select_related("obj__thing").first()

    assert p1.title is None
    assert p1.obj is None


@pytest.mark.django_db
def test_post_fetch_hook__prefetch_related() -> None:
    thing = Thing(name="foo", age=12, email="foo@bar.com")
    thing.save()

    obj = Object(thing=thing, identifier=0)
    obj.save()

    t1: Thing = Thing.objects.prefetch_related("objs").first()

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None
    assert next(iter(t1.objs.all())).identifier is None


@pytest.mark.django_db
def test_post_fetch_hook__prefetch_related__multiple() -> None:
    thing = Thing(name="foo", age=12, email="foo@bar.com")
    thing.save()

    obj = Object(thing=thing, identifier=0)
    obj.save()

    parent = Parent(obj=obj, title="bar")
    parent.save()

    t1: Thing = Thing.objects.prefetch_related("objs__parents").first()

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None

    o1 = next(iter(t1.objs.all()))
    assert o1.identifier is None

    p1 = next(iter(o1.parents.all()))
    assert p1.title is None


@pytest.mark.django_db
def test_post_fetch_hook__mix_of_select_and_prefetch_related() -> None:
    thing = Thing(name="foo", age=12, email="foo@bar.com")
    thing.save()

    obj = Object(thing=thing, identifier=0)
    obj.save()

    parent = Parent(obj=obj, title="bar")
    parent.save()

    o1: Object = Object.objects.select_related("thing").prefetch_related("parents").first()

    assert o1.identifier is None

    t1 = o1.thing

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None

    p1 = next(iter(o1.parents.all()))
    assert p1.title is None
