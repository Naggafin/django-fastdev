import pytest
from django.contrib.auth.models import User
from django.db.models import Q

from tests.models import SelfRef


@pytest.mark.django_db
def test_queryset_get_error_single():
    with pytest.raises(User.DoesNotExist) as e:
        User.objects.get(username__contains='a')

    assert str(e.value) == """User matching query does not exist.

Query kwargs:

    username__contains: 'a'"""


@pytest.mark.django_db
def test_queryset_get_error_single_args():
    with pytest.raises(User.DoesNotExist) as e:
        User.objects.get(Q(username__contains='a'))

    assert str(e.value) == """User matching query does not exist.

Query args:

    (<Q: (AND: ('username__contains', 'a'))>,)"""


@pytest.mark.django_db
def test_queryset_get_error_self_ref():
    selfref = SelfRef.objects.create()
    with pytest.raises(SelfRef.DoesNotExist) as e:
        SelfRef.objects.get(selfref=selfref)

    assert str(e.value) == """SelfRef matching query does not exist.

Query kwargs:

    selfref: <SelfRef pk=1>"""


@pytest.mark.django_db
def test_queryset_get_error_multi():
    User.objects.create(username='aa')
    User.objects.create(username='ab')
    with pytest.raises(User.MultipleObjectsReturned) as e:
        User.objects.get(username__contains='a')

    assert str(e.value) == """get() returned more than one User -- it returned 2!

Query kwargs:

    username__contains: 'a'"""


@pytest.mark.django_db
def test_queryset_get_error_multi_self_ref():
    parent = SelfRef.objects.create()
    SelfRef.objects.create(selfref=parent)
    SelfRef.objects.create(selfref=parent)
    with pytest.raises(SelfRef.MultipleObjectsReturned) as e:
        SelfRef.objects.get(selfref=parent)

    assert str(e.value) == """get() returned more than one SelfRef -- it returned 2!

Query kwargs:

    selfref: <SelfRef pk=1>"""
