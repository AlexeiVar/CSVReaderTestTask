import pytest

from utils import *

# Есть сомнения в необходимости этого файла ибо в test_definitions все это вызывается, но для полноты оставил

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


# тесты для aggregate
def test_aggregate_avg(make_new_list):
    result = aggregate_avg(make_new_list, 'price')
    assert result == 674

    result = aggregate_avg(make_new_list, 'rating')
    assert result == 4.67


def test_aggregate_max(make_new_list):
    result = aggregate_max(make_new_list, 'price')
    assert result == 1199

    result = aggregate_max(make_new_list, 'rating')
    assert result == 4.9


def test_aggregate_ming(make_new_list):
    result = aggregate_min(make_new_list, 'price')
    assert result == 199

    result = aggregate_min(make_new_list, 'rating')
    assert result == 4.4


# конец тестов для aggregate

# начало тестов для where
def test_where_equal(make_new_list):
    result = where_equal(make_new_list, 'brand', 'xiaomi', False)
    assert result == [{"name": 'redmi note 12', "brand": 'xiaomi', 'price': '199', 'rating': '4.6'},
                      {"name": 'poco x5 pro', "brand": 'xiaomi', 'price': '299', 'rating': '4.4'}
                      ]

    result = where_equal(make_new_list, 'price', float('299'), True)
    assert result == [{'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': 299.0, 'rating': '4.4'}]


def test_where_less(make_new_list):
    result = where_less(make_new_list, 'brand', 'b', False)
    assert result == [{"name": 'iphone 15 pro', "brand": 'apple', 'price': '999', 'rating': '4.9'}]

    result = where_less(make_new_list, 'price', float('500'), True)
    assert result == [{"name": 'redmi note 12', "brand": 'xiaomi', 'price': 199.0, 'rating': '4.6'},
                      {"name": 'poco x5 pro', "brand": 'xiaomi', 'price': 299.0, 'rating': '4.4'}
                      ]


def test_where_greater(make_new_list):
    result = where_greater(make_new_list, 'brand', 'b', False)
    assert result == [
        {"name": 'galaxy s23 ultra', "brand": 'samsung', 'price': '1199', 'rating': '4.8'},
        {"name": 'redmi note 12', "brand": 'xiaomi', 'price': '199', 'rating': '4.6'},
        {"name": 'poco x5 pro', "brand": 'xiaomi', 'price': '299', 'rating': '4.4'}
    ]

    result = where_greater(make_new_list, 'price', float('500'), True)
    assert result == [{"name": 'iphone 15 pro', "brand": 'apple', 'price': 999.0, 'rating': '4.9'},
                      {"name": 'galaxy s23 ultra', "brand": 'samsung', 'price': 1199.0, 'rating': '4.8'},
                      ]

# конец тестов для where

# order-by не тестируется поскольку, использует только встроенную функцию sorted
