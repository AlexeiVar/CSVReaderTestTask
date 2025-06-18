import csv


# Начало aggregate
def aggregate_avg(reader: csv.DictReader | list, column: str) -> float:
    total = 0
    average = 0
    for line in reader:
        total += 1
        average = average + float(line[column])
    result = round(average / total, 2)
    return result


def aggregate_min(reader: csv.DictReader | list, column: str) -> float:
    minimum = None
    for line in reader:
        if not minimum:
            minimum = float(line[column])
            continue
        if minimum > float(line[column]):
            minimum = float(line[column])
    result = minimum
    return result


def aggregate_max(reader: csv.DictReader | list, column: str) -> float:
    maximum = None
    for line in reader:
        if not maximum:
            maximum = float(line[column])
            continue
        if maximum < float(line[column]):
            maximum = float(line[column])
    result = maximum
    return result


aggregate_dict = {
    'avg': aggregate_avg,
    'min': aggregate_min,
    'max': aggregate_max
}


# Конец aggregate

# Начало where
def where_equal(reader: csv.DictReader | list, column: str, value: str | int | float, number: bool) -> list:
    data = []
    for line in reader:
        if number:
            line[column] = float(line[column])
        if line[column] == value:
            data.append(line)
    return data


def where_less(reader: csv.DictReader | list, column: str, value: str | int | float, number: bool) -> list:
    data = []
    for line in reader:
        if number:
            line[column] = float(line[column])
        if line[column] < value:
            data.append(line)
    return data


def where_greater(reader: csv.DictReader | list, column: str, value: str | int | float, number: bool) -> list:
    data = []
    for line in reader:
        if number:
            line[column] = float(line[column])
        if line[column] > value:
            data.append(line)
    return data


where_dict = {
    '=': where_equal,
    '<': where_less,
    '>': where_greater
}


# Конец where

# Начало order-by
def order_by_asc(unsorted: list, column: str) -> list:
    data = sorted(unsorted, key=lambda d: d[column])
    return data


def order_by_desc(unsorted: list, column: str) -> list:
    data = sorted(unsorted, key=lambda d: d[column], reverse=True)
    return data


order_by_dict = {
    'asc': order_by_asc,
    'desc': order_by_desc
}
# Конец order-by
