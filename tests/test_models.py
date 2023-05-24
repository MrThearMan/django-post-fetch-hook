import pytest

from post_fetch_hook.typing import Any
from tests.myapp.models import Object, Parent, Thing


@pytest.mark.django_db
def test_post_fetch_hook():
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
def test_post_fetch_values_hook():
    t0 = Thing(name="foo", age=12, email="foo@bar.com")

    assert t0.name == "foo"
    assert t0.age == 12
    assert t0.email == "foo@bar.com"

    t0.save()

    t1: dict[str, Any] = Thing.objects.values("name", "age").first()

    assert t1["name"] == "name"
    assert t1["age"] == "age"


@pytest.mark.django_db
def test_post_fetch_values_list_hook():
    t0 = Thing(name="foo", age=12, email="foo@bar.com")

    assert t0.name == "foo"
    assert t0.age == 12
    assert t0.email == "foo@bar.com"

    t0.save()

    t1: tuple[Any, ...] = Thing.objects.values_list("name", "age").first()

    assert t1[0] == "name"
    assert t1[1] == "age"


@pytest.mark.django_db
def test_post_fetch_values_list_flat_hook():
    t0 = Thing(name="foo", age=12, email="foo@bar.com")

    assert t0.name == "foo"
    assert t0.age == 12
    assert t0.email == "foo@bar.com"

    t0.save()

    t1: Any = Thing.objects.values_list("name", flat=True).first()

    assert t1 == "name"


@pytest.mark.django_db
def test_post_fetch_hook__get():
    Thing(name="foo", age=12, email="foo@bar.com").save()

    t1: Thing = Thing.objects.get(name="foo")

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None


@pytest.mark.django_db
def test_post_fetch_hook__first():
    Thing(name="foo", age=12, email="foo@bar.com").save()

    t1: Thing = Thing.objects.first()

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None


@pytest.mark.django_db
def test_post_fetch_hook__last():
    Thing(name="foo", age=12, email="foo@bar.com").save()

    t1: Thing = Thing.objects.last()

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None


@pytest.mark.django_db
def test_post_fetch_hook__iter():
    Thing(name="foo", age=12, email="foo@bar.com").save()

    t1: list[Thing] = list(Thing.objects.all())

    assert t1[0].name is None
    assert t1[0].age is None
    assert t1[0].email is None


@pytest.mark.django_db
def test_post_fetch_hook__select_related():
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
def test_post_fetch_hook__select_related__all():
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
def test_post_fetch_hook__select_related__multiple():
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
def test_post_fetch_hook__select_related__null_relation():
    parent = Parent(obj=None, title="bar")
    parent.save()

    p1: Parent = Parent.objects.select_related("obj__thing").first()

    assert p1.title is None
    assert p1.obj is None


@pytest.mark.django_db
def test_post_fetch_hook__prefetch_related():
    thing = Thing(name="foo", age=12, email="foo@bar.com")
    thing.save()

    obj = Object(thing=thing, identifier=0)
    obj.save()

    t1: Thing = Thing.objects.prefetch_related("objs").first()

    assert t1.name is None
    assert t1.age is None
    assert t1.email is None
    assert list(t1.objs.all())[0].identifier is None


@pytest.mark.django_db
def test_post_fetch_hook__prefetch_related__multiple():
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

    o1 = list(t1.objs.all())[0]
    assert o1.identifier is None

    p1 = list(o1.parents.all())[0]
    assert p1.title is None


@pytest.mark.django_db
def test_post_fetch_hook__mix_of_select_and_prefetch_related():
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

    p1 = list(o1.parents.all())[0]
    assert p1.title is None
