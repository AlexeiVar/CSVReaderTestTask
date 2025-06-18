import pytest

from definitions import *


# Некоторые функции меняют лист внутри себя, поэтому для изоляции делаем новые листы
@pytest.fixture()
def make_new_list():
    test_list = [
        {"name": 'iphone 15 pro', "brand": 'apple', 'price': '999', 'rating': '4.9'},
        {"name": 'galaxy s23 ultra', "brand": 'samsung', 'price': '1199', 'rating': '4.8'},
        {"name": 'redmi note 12', "brand": 'xiaomi', 'price': '199', 'rating': '4.6'},
        {"name": 'poco x5 pro', "brand": 'xiaomi', 'price': '299', 'rating': '4.4'}
    ]
    return test_list


def test_aggregate(make_new_list):
    result = aggregate(make_new_list, 'rating=avg')
    assert result == {'avg': [4.67]}

    result = aggregate(make_new_list, 'rating=min')
    assert result == {'min': [4.4]}

    result = aggregate(make_new_list, 'rating=max')
    assert result == {'max': [4.9]}

    with pytest.raises(ValueError, match='aggregate does not accept this operation'):
        aggregate(make_new_list, 'rating=invalid')

    with pytest.raises(ValueError, match='aggregate only supports numbers'):
        aggregate(make_new_list, 'brand=avg')


def test_where(make_new_list):
    result = where(make_new_list, 'brand=xiaomi')
    assert result == [
        {"name": 'redmi note 12', "brand": 'xiaomi', 'price': '199', 'rating': '4.6'},
        {"name": 'poco x5 pro', "brand": 'xiaomi', 'price': '299', 'rating': '4.4'}
    ]
    result = where(make_new_list, 'price<300')
    assert result == [
        {"name": 'redmi note 12', "brand": 'xiaomi', 'price': 199.0, 'rating': '4.6'},
        {"name": 'poco x5 pro', "brand": 'xiaomi', 'price': 299.0, 'rating': '4.4'}
    ]
    result = where(make_new_list, 'price>300')
    assert result == [
        {"name": 'iphone 15 pro', "brand": 'apple', 'price': 999.0, 'rating': '4.9'},
        {"name": 'galaxy s23 ultra', "brand": 'samsung', 'price': 1199.0, 'rating': '4.8'},
    ]


def test_order_by(make_new_list):
    result = order_by(make_new_list, 'price=desc')
    assert result == [
        {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': 1199.0, 'rating': '4.8'},
        {'name': 'iphone 15 pro', 'brand': 'apple', 'price': 999.0, 'rating': '4.9'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': 299.0, 'rating': '4.4'},
        {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': 199.0, 'rating': '4.6'}]
    result = order_by(make_new_list, 'price=asc')
    assert result == [{'name': 'redmi note 12', 'brand': 'xiaomi', 'price': 199.0, 'rating': '4.6'},
                      {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': 299.0, 'rating': '4.4'},
                      {'name': 'iphone 15 pro', 'brand': 'apple', 'price': 999.0, 'rating': '4.9'},
                      {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': 1199.0, 'rating': '4.8'}]


def test_where_to_aggregate(make_new_list):
    intermediate = where(make_new_list, 'brand=xiaomi')
    result = aggregate(intermediate, 'rating=avg')
    assert result == {'avg': [4.5]}

    intermediate = where(make_new_list, 'price<300')
    result = aggregate(intermediate, 'rating=avg')
    assert result == {'avg': [4.5]}

    intermediate = where(make_new_list, 'price>300')
    result = aggregate(intermediate, 'rating=avg')
    assert result == {'avg': [4.85]}


def test_where_to_order(make_new_list):
    intermediate = where(make_new_list, 'brand=xiaomi')
    result = order_by(intermediate, 'price=asc')
    assert result == [{'name': 'redmi note 12', 'brand': 'xiaomi', 'price': 199.0, 'rating': '4.6'},
                      {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': 299.0, 'rating': '4.4'}
                      ]

    intermediate = where(make_new_list, 'price<300')
    result = order_by(intermediate, 'price=desc')
    assert result == [
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': 299.0, 'rating': '4.4'},
        {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': 199.0, 'rating': '4.6'}
    ]

    intermediate = where(make_new_list, 'price>300')
    result = order_by(intermediate, 'price=desc')
    assert result == [
        {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': 1199.0, 'rating': '4.8'},
        {'name': 'iphone 15 pro', 'brand': 'apple', 'price': 999.0, 'rating': '4.9'}
    ]
